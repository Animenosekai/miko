"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.deactivate = exports.activate = void 0;
const cp = require("child_process");
// The module 'vscode' contains the VS Code extensibility API
// Import the module and reference it with the alias vscode in your code below
const vscode = require("vscode");
const execMiko = (file, noself) => {
    const pythonPath = String(vscode.workspace.getConfiguration("python").get("pythonPath"));
    console.log(`Current Python path: ${pythonPath}`);
    const args = ["-m", "miko", "clean", "-f", file, "-o", file];
    if (noself) {
        args.push("--noself");
    }
    return new Promise((resolve, reject) => {
        cp.execFile(pythonPath, args, (err, out) => {
            if (err) {
                return reject(err);
            }
            return resolve(out);
        });
    });
};
// this method is called when your extension is activated
// your extension is activated the very first time the command is executed
function activate(context) {
    const disposableFormat = vscode.commands.registerCommand('miko.format', () => {
        if (!vscode.window.activeTextEditor) {
            return;
        }
        vscode.window.activeTextEditor.document.save();
        execMiko(vscode.window.activeTextEditor.document.fileName, String(vscode.workspace.getConfiguration("miko-docs").get("noself")) === "true")
            .then(() => {
            // if (vscode.window.activeTextEditor) {
            //     vscode.window.activeTextEditor.document.save();
            // }
            vscode.window.showInformationMessage('🍡 Successfully formatted the current file using Miko!');
        })
            .catch(err => {
            vscode.window.showErrorMessage(err.message);
        });
    });
    context.subscriptions.push(disposableFormat);
    const disposableFormatAll = vscode.commands.registerCommand('miko.formatAll', () => {
        vscode.window.visibleTextEditors.forEach(editor => {
            editor.document.save();
            execMiko(editor.document.fileName, String(vscode.workspace.getConfiguration("miko-docs").get("noself")) === "true")
                .then(() => {
                // editor.document.save();
                let splitted = editor.document.fileName.split("/");
                splitted = splitted[splitted.length - 1].split("\\"); // windows
                vscode.window.showInformationMessage(`🍡 Successfully formatted "${splitted[splitted.length - 1]}" using Miko!`);
            })
                .catch(err => {
                vscode.window.showErrorMessage(err.message);
            });
        });
    });
    context.subscriptions.push(disposableFormatAll);
}
exports.activate = activate;
// this method is called when your extension is deactivated
function deactivate() { }
exports.deactivate = deactivate;
//# sourceMappingURL=extension.js.map