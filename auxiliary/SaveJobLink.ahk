#Requires AutoHotkey v2.0

; Shortcut Trigger: Ctrl + Alt + C
^!c::
{
    ; Backing up current clipboard contents
    ClipSaved := ClipboardAll()
    
    ; Clearing the clipboard and simulating Ctrl+C to copy highlighted text
    A_Clipboard := ""
    Send("^c")
    
    ; Waiting to ensure copy
if ClipWait(1)
    {
        ; Getting clean, absolute path
        SplitPath(A_ScriptDir, , &ParentDir) ; This grabs the parent directory
        FilePath := ParentDir "\data\process\job.txt"
        
        ; Ensure the 'data' folder actually exists
        SplitPath(FilePath, , &FileDir)
        if !DirExist(FileDir)
            DirCreate(FileDir)
        
        ; Appending the data
        FileAppend(A_Clipboard "`n", FilePath, "UTF-8")
    }
    
    ; Restoring original clipboard
    A_Clipboard := ClipSaved
    ClipSaved := "" ; Free memory
}