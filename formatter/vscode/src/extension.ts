import * as cp from "child_process";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

const mikoOutputChannel = vscode.window.createOutputChannel("Miko Docs");

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
const execMiko = (file: string, indent: number, noself: boolean, flagPrefix: string, safe: boolean) => {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
        return Promise.reject(new Error("🕊️ Could not find a Python interpreter. Please set the \"python.defaultInterpreterPath\" setting to the path of your Python interpreter."));
    }
    const args = ["-m", "miko", "clean", file, "--output", file, "--indent", Math.floor(indent).toString(), "--flag-prefix", flagPrefix];
    if (noself) {
        args.push("--noself");
    }
    if (safe) {
        args.push("--safe");
    }

    mikoOutputChannel.appendLine(`Calling python with arguments: ${args.join(" ")}`);

    return new Promise<string>((resolve, reject) => {
        cp.execFile(pythonPath, args, (err, out) => {
            if (err) {
                return reject(err);
            }
            return resolve(out);
        });
    });
}

export function activate(context: vscode.ExtensionContext) {
    const pythonPath = getPythonPath();
    if (!pythonPath) {
        vscode.window.showErrorMessage("🕊️ Could not find a Python interpreter. Please set the \"python.defaultInterpreterPath\" setting to the path of your Python interpreter.");
        return;
    }
    mikoOutputChannel.appendLine("Checking if the `miko` formatter is installed...")
    cp.execFile(pythonPath, ["-m", "miko", "--version"], (err, out) => {
        if (err) {
            mikoOutputChannel.appendLine("The `miko` formatter doesn't seem to be installed on the system.")
            vscode.window.showErrorMessage("The `miko` formatter doesn't seem to be installed on your system. Do you want to install it?", "Yes", "No")
                .then((value) => {
                    mikoOutputChannel.appendLine(`The user chose: ${value}`)
                    if (value === "Yes") {
                        mikoOutputChannel.appendLine("Installing the `miko` formatter...")
                        cp.execFile(pythonPath, ["-m", "pip", "install", "--upgrade", "miko"], (err, out) => {
                            if (err) {
                                mikoOutputChannel.appendLine(`An error occured while installing the formatter: ${err} (${err.message})`)
                                vscode.window.showErrorMessage("🕊️ Could not install the `miko` formatter. Please install it manually using `pip install --upgrade miko`.");
                                return;
                            }
                            mikoOutputChannel.appendLine(out)
                            mikoOutputChannel.appendLine("Successfully installed the formatter")
                            vscode.window.showInformationMessage("🍡 Successfully installed the `miko` formatter!");
                        });
                    }
                })
            return;
        }
        mikoOutputChannel.appendLine(`The current version of the formatter is: ${out}`)
        if (out[0] === "m" || out[0] == "1") {
            mikoOutputChannel.appendLine("This is an outdated version of the `miko` formatter.")
            vscode.window.showErrorMessage("The installed `miko` formatter is outdated. Do you want to update it?", "Yes", "No")
                .then((value) => {
                    mikoOutputChannel.appendLine(`The user chose: ${value}`)
                    if (value === "Yes") {
                        cp.execFile(pythonPath, ["-m", "pip", "install", "--upgrade", "miko"], (err, out) => {
                            if (err) {
                                mikoOutputChannel.appendLine(`An error occured while installing the formatter: ${err} (${err.message})`)
                                vscode.window.showErrorMessage("🕊️ Could not install the `miko` formatter. Please install it manually using `pip install--upgrade miko`.");
                                return;
                            }
                            mikoOutputChannel.appendLine(out)
                            mikoOutputChannel.appendLine("Successfully installed the formatter")
                            vscode.window.showInformationMessage("🍡 Successfully installed the `miko` formatter!");
                        });
                    }
                })
            return;
        }
    });

    const config = vscode.workspace.getConfiguration("miko-docs");

    const noself = config.get<boolean>("noSelf") || true;
    const flagPrefix = config.get<string>("flagPrefix") || "!";
    const safe = config.get<boolean>("safe") || true;

    const disposableFormat = vscode.commands.registerCommand('miko.format', () => {
        if (!vscode.window.activeTextEditor) {
            mikoOutputChannel.appendLine("No active text editor.")
            return // We don't have any opened text editors
        }

        // Save the current file
        const document = vscode.window.activeTextEditor.document;
        mikoOutputChannel.appendLine("Saving the current file");
        document.save();

        let indent = vscode.window.activeTextEditor.options.tabSize || 4;
        if (typeof indent === 'string') {
            indent = 4;
        } else {
            indent = Math.floor(indent);
        }
        mikoOutputChannel.appendLine(`Indentation level: ${indent}`)

        // Format the current file
        execMiko(document.fileName, indent, noself, flagPrefix, safe)
            .then(() => {
                vscode.window.showInformationMessage('🍡 Successfully formatted the current file using Miko!');
            })
            .catch(err => {
                vscode.window.showErrorMessage(err.message);
            });
    });
    context.subscriptions.push(disposableFormat);

    const disposableFormatAll = vscode.commands.registerCommand('miko.formatAll', () => {
        vscode.window.visibleTextEditors.forEach(editor => {
            mikoOutputChannel.appendLine(`Saving ${editor.document.fileName}`);
            editor.document.save();

            let indent = editor.options.tabSize || 4;
            if (typeof indent === 'string') {
                indent = 4; // 4 by default
            } else {
                indent = Math.floor(indent);
            }
            mikoOutputChannel.appendLine(`Indentation level for "${editor.document.fileName}": ${indent} `)

            execMiko(editor.document.fileName, indent, noself, flagPrefix, safe)
                .then(() => {
                    // editor.document.save();
                    let splitted = editor.document.fileName.split("/")
                    splitted = splitted[splitted.length - 1].split("\\") // windows
                    vscode.window.showInformationMessage(`🍡 Successfully formatted "${splitted[splitted.length - 1]}" using Miko!`);
                })
                .catch(err => {
                    vscode.window.showErrorMessage(err.message);
                });
        })
    });
    context.subscriptions.push(disposableFormatAll);
}

// this method is called when your extension is deactivated
export function deactivate() { }