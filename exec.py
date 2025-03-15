import argparse
import FreeSimpleGUI as psg
import pdfdye
import pikepdf

layout = [
    [ psg.Text("Input PDF:", size = 10), psg.Input(key = "input"), psg.FileBrowse(file_types = [("PDF Files", ".pdf")]) ],
    [ psg.Text("Red:", size = 10), psg.DropDown(list(range(256)), default_value = "0", key = "red") ],
    [ psg.Text("Green:", size = 10), psg.DropDown(list(range(256)), default_value = "0", key = "green") ],
    [ psg.Text("Blue:", size = 10), psg.DropDown(list(range(256)), default_value = "0", key = "blue") ],
    [ psg.Text("Output PDF:", size = 10), psg.Input(key = "output"), psg.FileSaveAs(file_types = [("PDF Files", ".pdf")]) ],
    [ psg.Button("Submit", key = "submit") ]
]

window = psg.Window("", layout, grab_anywhere = True, font = "-size 12")

while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "submit"):
        redHex = str(hex(int(values["red"])))[2:].upper().zfill(2)
        greenHex = str(hex(int(values["green"])))[2:].upper().zfill(2)
        blueHex = str(hex(int(values["blue"])))[2:].upper().zfill(2)
        colHex = redHex + greenHex + blueHex
        pdf = pikepdf.open(values["input"])
        pdfdye.mangle_pdf(pdf, pdfdye.parse_color(colHex))
        pdf.save(values["output"])
        break