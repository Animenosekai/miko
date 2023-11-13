import * as cp from "child_process";
import * as path from "path";
import * as vscode from 'vscode';

const mikoOutputChannel = vscode.window.createOutputChannel("Miko Docs");
const mikoOverviewScheme = "miko-docs-overview"
// Contains the different error messages that can be displayed to the user.
const mikoErrorMsg = {
    pythonNotFound: "🕊️ Could not find a Python interpreter. Please set the \"python.defaultInterpreterPath\" setting to the path of your Python interpreter.",
    mikoNotFound: "The `miko` formatter doesn't seem to be installed on your system. Do you want to install it?",
    installError: "🕊️ Could not install the `miko` formatter. Please install it manually using `pip install --upgrade miko`.",
    mikoOutdated: "The installed `miko` formatter is outdated. Do you want to update it?",
    notPythonFile: "The current file is not a Python file.",
    noFileName: "The current file has no name."
}

// Returns the path of the Python interpreter.
const getPythonPath = () => {
    const pythonConfig = vscode.workspace.getConfiguration('python');
    const pythonPath = pythonConfig.get<string>('defaultInterpreterPath');
    mikoOutputChannel.appendLine(`Python Executable: ${pythonPath}`)
    return pythonPath;
}

/**
 * Executes the Miko formatter on the specified file.
 * @param file - The path of the file to format.
 * @param indent - The number of spaces to use for indentation.
 * @param noself - Whether to exclude the "self" parameter in method signatures.
 * @param flagPrefix - The prefix to use for flag arguments.
 * @param safe - Whether to use safe type annotations and exceptions.
 * @returns A Promise that resolves to the output of the formatter.
 */
const execMikoClean = (file: string, indent: number, noself: boolean, flagPrefix: string, safe: boolean, useBlack: boolean) => {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
        return Promise.reject(new Error(mikoErrorMsg.pythonNotFound));
    }
    // const args = ["-m", "miko", "clean", file, "--output", file, "--indent", Math.floor(indent).toString(), "--flag-prefix", flagPrefix];
    const args = ["-m", "miko", "clean", file, "--indent", Math.floor(indent).toString(), "--flag-prefix", flagPrefix];
    if (noself) {
        args.push("--noself");
    }
    if (safe) {
        args.push("--safe");
    }
    if (useBlack) {
        args.push("--use-black");
    }

    mikoOutputChannel.appendLine(`Calling python with arguments: ${args.join(" ")}`);

    return new Promise<string>((resolve, reject) => vscode.window.withProgress({
        location: vscode.ProgressLocation.Window,
        title: "Formatting file...",
        cancellable: false
    }, (progress, token) => {
        progress.report({ increment: 0 });
        return new Promise<string>((res, rej) => {
            cp.execFile(pythonPath, args, (err, out) => {
                progress.report({ increment: 100 });
                return err ? rej(err) : res(out);
            });
        }).then((result) => {
            resolve(result);
        }).catch((err) => {
            reject(err);
        })
    }));
}

const installMiko = (pythonPath: string) => {
    mikoOutputChannel.appendLine("Installing the `miko` formatter...")
    return vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Installing `miko`",
        cancellable: false
    }, (progress, token) => {
        return new Promise<void>((resolve, reject) => {
            cp.execFile(pythonPath, ["-m", "pip", "install", "--upgrade", "miko"], (err, out) => {
                if (err) {
                    mikoOutputChannel.appendLine(`An error occured while installing the formatter: ${err} (${err.message})`)
                    vscode.window.showErrorMessage(mikoErrorMsg.installError);
                    return reject();
                }
                mikoOutputChannel.appendLine(out)
                mikoOutputChannel.appendLine("Successfully installed the formatter")
                vscode.window.showInformationMessage("🍡 Successfully installed the `miko` formatter!");
                return resolve();
            })
        })
    })
}

/**
 * Checks if the Miko formatter is installed and up-to-date.
 * @param pythonPath - The path of the Python interpreter.
 */
const checkInstallation = (pythonPath: string) => {
    mikoOutputChannel.appendLine("Checking if the `miko` formatter is installed...")
    cp.execFile(pythonPath, ["-m", "miko", "--version"], (err, out) => {
        if (err) {
            mikoOutputChannel.appendLine("The `miko` formatter doesn't seem to be installed on the system.")
            vscode.window.showErrorMessage(mikoErrorMsg.mikoNotFound, "Yes", "No")
                .then((value) => {
                    mikoOutputChannel.appendLine(`The user chose: ${value}`)
                    if (value === "Yes") {
                        return installMiko(pythonPath);
                    }
                })
            return;
        }
        mikoOutputChannel.appendLine(`The current version of the formatter is: ${out}`)
        // The version used to follow the format : `miko v<version>`
        if (out[0] === "m" || out[0] == "1") {
            mikoOutputChannel.appendLine("This is an outdated version of the `miko` formatter.")
            vscode.window.showErrorMessage(mikoErrorMsg.mikoOutdated, "Yes", "No")
                .then((value) => {
                    mikoOutputChannel.appendLine(`The user chose: ${value}`)
                    if (value === "Yes") {
                        return installMiko(pythonPath);
                    }
                })
            return;
        }
    });
}

export function activate(context: vscode.ExtensionContext) {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
        vscode.window.showErrorMessage(mikoErrorMsg.pythonNotFound);
        return;
    }
    checkInstallation(pythonPath);

    vscode.languages.registerDocumentFormattingEditProvider('python', {
        provideDocumentFormattingEdits(document: vscode.TextDocument): Promise<vscode.TextEdit[]> {
            mikoOutputChannel.appendLine("");
            mikoOutputChannel.appendLine("`format` command coming from vscode: `provideDocumentFormattingEdits`");
            const config = vscode.workspace.getConfiguration("miko-docs");
            if (!(config.get<boolean>("format.enable"))) {
                mikoOutputChannel.appendLine("config `format.enable` is set to `false`");
                return Promise.resolve([]);
            }

            const text = document.getText();

            let indent = vscode.window.activeTextEditor?.options?.tabSize || 4;
            if (typeof indent === 'string') {
                // Might happen if `auto` is selected
                indent = 4;
            } else {
                indent = Math.floor(indent);
            }
            mikoOutputChannel.appendLine(`Indentation level: ${indent}`)

            const noself = config.get<boolean>("format.noSelf") || true;
            const flagPrefix = config.get<string>("format.flagPrefix") || "!";
            const useBlack = config.get<boolean>("format.useBlack") || false;
            const safe = config.get<boolean>("safe") || true;

            const documentStart = document.lineAt(0).range.start;
            const documentEnd = document.lineAt(document.lineCount - 1).range.end;
            const documentRange = new vscode.Range(documentStart, documentEnd);

            return execMikoClean(text, indent, noself, flagPrefix, safe, useBlack)
                .then((result) => {
                    vscode.window.showInformationMessage('🍡 Successfully formatted the current file using Miko!');
                    return [vscode.TextEdit.replace(documentRange, result)];
                })
                .catch(err => {
                    vscode.window.showErrorMessage(err.message);
                    return [];
                });
        }
    });

    const mikoFormat = vscode.commands.registerCommand('miko-docs.format', () => {
        mikoOutputChannel.appendLine("");
        mikoOutputChannel.appendLine("`format` command coming from user: `miko-docs.format`");

        if (!vscode.window.activeTextEditor) {
            mikoOutputChannel.appendLine("No active text editor.")
            return // We don't have any opened text editors
        }

        // Save the current file
        const document = vscode.window.activeTextEditor.document;
        if (document.languageId !== "python") {
            mikoOutputChannel.appendLine("The current file is not a Python file.")
            vscode.window.showErrorMessage(mikoErrorMsg.notPythonFile)
            return
        }

        if (!document.fileName) {
            mikoOutputChannel.appendLine("The current file has no name.")
            vscode.window.showErrorMessage(mikoErrorMsg.noFileName)
            return
        }

        mikoOutputChannel.appendLine("Saving the current file");
        document.save();

        let indent = vscode.window.activeTextEditor.options.tabSize || 4;
        if (typeof indent === 'string') {
            indent = 4;
        } else {
            indent = Math.floor(indent);
        }
        mikoOutputChannel.appendLine(`Indentation level: ${indent}`)

        const config = vscode.workspace.getConfiguration("miko-docs");

        const noself = config.get<boolean>("format.noSelf") || true;
        const flagPrefix = config.get<string>("format.flagPrefix") || "!";
        const useBlack = config.get<boolean>("format.useBlack") || false;
        const safe = config.get<boolean>("safe") || true;

        // Format the current file
        execMikoClean(document.fileName, indent, noself, flagPrefix, safe, useBlack)
            .then((result) => {
                const edit = new vscode.WorkspaceEdit();

                const documentStart = document.lineAt(0).range.start;
                const documentEnd = document.lineAt(document.lineCount - 1).range.end;
                const documentRange = new vscode.Range(documentStart, documentEnd);

                edit.replace(document.uri, documentRange, result);
                vscode.workspace.applyEdit(edit);
                vscode.window.showInformationMessage('🍡 Successfully formatted the current file using Miko!');
            })
            .catch(err => {
                vscode.window.showErrorMessage(err.message);
            });
    });
    context.subscriptions.push(mikoFormat);

    const mikoFormatAll = vscode.commands.registerCommand('miko-docs.formatAll', () => {
        mikoOutputChannel.appendLine("");
        mikoOutputChannel.appendLine("`format` command coming from user: `miko-docs.formatAll`");

        vscode.window.visibleTextEditors.forEach(editor => {
            const document = editor.document;
            if (document.languageId !== "python") {
                mikoOutputChannel.appendLine("Skipping file which is not a Python file.")
                return
            }

            if (!document.fileName) {
                mikoOutputChannel.appendLine("Skipping file which has no name.")
                return
            }

            mikoOutputChannel.appendLine("Saving the current file");
            document.save();

            let indent = editor.options.tabSize || 4;
            if (typeof indent === 'string') {
                indent = 4;
            } else {
                indent = Math.floor(indent);
            }
            mikoOutputChannel.appendLine(`Indentation level: ${indent}`)

            const config = vscode.workspace.getConfiguration("miko-docs");

            const noself = config.get<boolean>("format.noSelf") || true;
            const flagPrefix = config.get<string>("format.flagPrefix") || "!";
            const useBlack = config.get<boolean>("format.useBlack") || false;
            const safe = config.get<boolean>("safe") || true;

            execMikoClean(editor.document.fileName, indent, noself, flagPrefix, safe, useBlack)
                .then((result) => {
                    const edit = new vscode.WorkspaceEdit();

                    const documentStart = document.lineAt(0).range.start;
                    const documentEnd = document.lineAt(document.lineCount - 1).range.end;
                    const documentRange = new vscode.Range(documentStart, documentEnd);

                    edit.replace(document.uri, documentRange, result);
                    vscode.workspace.applyEdit(edit);

                    let splitted = editor.document.fileName.split("/")
                    splitted = splitted[splitted.length - 1].split("\\") // windows
                    vscode.window.showInformationMessage(`🍡 Successfully formatted "${splitted[splitted.length - 1]}" using Miko!`);
                })
                .catch(err => {
                    vscode.window.showErrorMessage(err.message);
                });
        })
    });
    context.subscriptions.push(mikoFormatAll);


    const overviewProvider = new class implements vscode.TextDocumentContentProvider {
        // emitter and its event
        onDidChangeEmitter = new vscode.EventEmitter<vscode.Uri>();
        onDidChange = this.onDidChangeEmitter.event;

        provideTextDocumentContent(uri: vscode.Uri): Promise<string> {
            const pythonPath = getPythonPath();
            if (!pythonPath) {
                return Promise.reject(new Error(mikoErrorMsg.pythonNotFound));
            }

            const fileURI = uri.path.slice(0, -3);
            // Check that this is a Python file
            if (!(fileURI.endsWith(".py") || fileURI.endsWith(".pyw"))) {
                vscode.window.showWarningMessage("The current file might not be a Python file.")
            }


            const args = ["-m", "miko", "overview", fileURI];

            const config = vscode.workspace.getConfiguration("miko-docs");
            const includePrivate = config.get<boolean>("overview.includePrivate") || true;
            const safe = config.get<boolean>("safe") || true;

            if (includePrivate) {
                args.push("--include-private");
            }
            if (safe) {
                args.push("--safe");
            }

            mikoOutputChannel.appendLine(`Calling python with arguments: ${args.join(" ")}`);

            return new Promise<string>((resolve, reject) => {
                let opt: cp.ProcessEnvOptions = {};
                // if (vscode.workspace.workspaceFolders) {
                //     opt.cwd = vscode.workspace.workspaceFolders[0].uri.fsPath;
                // }
                opt.cwd = path.dirname(fileURI);
                return resolve(vscode.window.withProgress({
                    location: vscode.ProgressLocation.Window,
                    cancellable: false,
                    title: "Generating overview..."
                }, (progress, token) => {
                    progress.report({ increment: 0 });
                    return new Promise((resolve, reject) => {
                        cp.execFile(pythonPath, args, opt, (err, out) => {
                            progress.report({ increment: 100 });
                            if (err) {
                                // return reject(err);
                                return resolve(`\`\`\`python\n${err.message}\n\`\`\``);
                            }
                            return resolve(out);
                        });
                    })
                }))

            });
        }
    };
    context.subscriptions.push(vscode.workspace.registerTextDocumentContentProvider(mikoOverviewScheme, overviewProvider));

    const mikoOverview = vscode.commands.registerCommand('miko-docs.overview', async () => {
        mikoOutputChannel.appendLine("");
        mikoOutputChannel.appendLine("`overview` command coming from user: `miko-docs.overview`");

        if (!vscode.window.activeTextEditor) {
            mikoOutputChannel.appendLine("No active text editor")
            return // We don't have any opened text editors
        }

        // Save the current file
        const document = vscode.window.activeTextEditor.document;
        mikoOutputChannel.appendLine("Saving the current file");
        document.save();

        const uri = vscode.Uri.parse(`${mikoOverviewScheme}:` + document.uri.fsPath + ".md");
        const doc = await vscode.workspace.openTextDocument(uri); // calls back into the provider
        vscode.commands.executeCommand("markdown.showPreviewToSide", doc.uri);
        // const editor = await vscode.window.showTextDocument(doc, { preview: true, viewColumn: vscode.ViewColumn.Beside });
    });
    context.subscriptions.push(mikoOverview);
}

// this method is called when your extension is deactivated
export function deactivate() { }