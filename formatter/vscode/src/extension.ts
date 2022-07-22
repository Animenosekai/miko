import * as cp from "child_process";
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
import * as vscode from 'vscode';

const execZero = (file: string, noself: boolean) => {
    const pythonPath = String(vscode.workspace.getConfiguration("python").get("pythonPath"));
    console.log(`Current Python path: ${pythonPath}`);
    const args = ["-m", "zero", "clean", "-f", file, "-o", file]
    if (noself) {
        args.push("--noself");
    }
    return new Promise<string>((resolve, reject) => {
        cp.execFile(pythonPath, args, (err, out) => {
            if (err) {
                return reject(err);
            }
            return resolve(out);
        });
    });
}

// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    const disposableFormat = vscode.commands.registerCommand('zero.format', () => {
        if (!vscode.window.activeTextEditor) { return }
        vscode.window.activeTextEditor.document.save();
        execZero(vscode.window.activeTextEditor.document.fileName, String(vscode.workspace.getConfiguration("zero-docs").get("noself")) === "true")
            .then(() => {
                // if (vscode.window.activeTextEditor) {
                //     vscode.window.activeTextEditor.document.save();
                // }
                vscode.window.showInformationMessage('🍡 Successfully formatted the current file using Zero!');
            })
            .catch(err => {
                vscode.window.showErrorMessage(err.message);
            });
    });
    context.subscriptions.push(disposableFormat);

    const disposableFormatAll = vscode.commands.registerCommand('zero.formatAll', () => {
        vscode.window.visibleTextEditors.forEach(editor => {
            editor.document.save();
            execZero(editor.document.fileName, String(vscode.workspace.getConfiguration("zero-docs").get("noself")) === "true")
                .then(() => {
                    // editor.document.save();
                    let splitted = editor.document.fileName.split("/")
                    splitted = splitted[splitted.length - 1].split("\\") // windows
                    vscode.window.showInformationMessage(`🍡 Successfully formatted "${splitted[splitted.length - 1]}" using Zero!`);
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