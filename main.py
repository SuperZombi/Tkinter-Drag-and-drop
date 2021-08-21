import os
from TkinterDnD2 import *
from tkinter import *

def Drag_and_drop(title="TkinterDnD Canvas", comment='Drag and drop files here:', icon=None, sort=False):
    root = TkinterDnD.Tk()
    root.withdraw()
    root.title(title)
    if icon:
        root.iconbitmap(icon)

    def okay():
        global temp
        if sort:
            temp = {'files':[], 'folders':[]}
            for i in canvas.filenames:
                if not canvas.filenames[i] in temp:
                    if os.path.isdir(canvas.filenames[i]):
                        if not canvas.filenames[i] in temp['folders']:
                            temp['folders'].append(canvas.filenames[i])
                    else:
                        if not canvas.filenames[i] in temp['files']:
                            temp['files'].append(canvas.filenames[i])
            if len(temp['files']) == 0 and len(temp['folders']) == 0:
                temp = {}
        else:
            temp = []
            for i in canvas.filenames:
                if not canvas.filenames[i] in temp:
                    temp.append(canvas.filenames[i])
        root.quit()

    root.grid_rowconfigure(1, weight=1, minsize=250)
    root.grid_columnconfigure(0, weight=1, minsize=300)

    Label(root, text=comment).grid(
                        row=0, column=0, padx=10, pady=5)
    buttonbox = Frame(root)
    buttonbox.grid(row=2, column=0, columnspan=2, pady=5)
    Button(buttonbox, text='OK', command=okay).pack(
                        side=LEFT, padx=5)

    file_icon = PhotoImage(data='R0lGODlhGAAYAKIAANnZ2TMzM////wAAAJmZmf///////////yH5BAEAAAAALAA'
            'AAAAYABgAAAPACBi63IqgC4GiyxwogaAbKLrMgSKBoBoousyBogEACIGiyxwoKgGAECI'
            '4uiyCExMTOACBosuNpDoAGCI4uiyCIkREOACBosutSDoAgSI4usyCIjQAGCi63Iw0ACE'
            'oOLrMgiI0ABgoutyMNAAhKDi6zIIiNAAYKLrcjDQAISg4usyCIjQAGCi63Iw0AIGiiqP'
            'LIyhCA4CBosvNSAMQKKo4ujyCIjQAGCi63Iw0AIGiy81IAxCBpMu9GAMAgKPL3QgJADs'
            '=')
    folder_icon = PhotoImage(data='R0lGODlhGAAYAKECAAAAAPD/gP///////yH+EUNyZWF0ZWQgd2l0aCBHSU1QA'
            'CH5BAEKAAIALAAAAAAYABgAAAJClI+pK+DvGINQKhCyztEavGmd5IQmYJXmhi7UC8frH'
            'EL0Hdj4rO/n41v1giIgkWU8cpLK4dFJhAalvpj1is16toICADs=')

    frame=Frame(root, height=300)
    frame.grid(row=1,column=1, sticky='news')

    canvas = Canvas(root, name='dnd_canvas', bg='white', relief='sunken',
                    bd=1, highlightthickness=1, takefocus=True, width=600, scrollregion=(0,0,0,0))
    
    vbar=Scrollbar(frame,orient=VERTICAL)
    vbar.pack(side=RIGHT,fill=Y)
    vbar.config(command=canvas.yview)

    canvas.config(yscrollcommand=vbar.set)
    canvas.grid(row=1, column=0, padx=5, pady=5, sticky='news')




    # store the filename associated with each canvas item in a dictionary
    canvas.filenames = {}
    # store the next icon's x and y coordinates in a list
    canvas.nextcoords = [50, 20]
    # add a boolean flag to the canvas which can be used to disable
    # files from the canvas being dropped on the canvas again
    canvas.dragging = False

    def add_file(filename):
        if not filename in canvas.filenames.values():
            #print(filename)
            icon = file_icon
            if os.path.isdir(filename):
                icon = folder_icon
            id1 = canvas.create_image(canvas.nextcoords[0], canvas.nextcoords[1],
                                        image=icon, anchor='n', tags=('file',))
            id2 = canvas.create_text(canvas.nextcoords[0], canvas.nextcoords[1] + 30,
                                        text=os.path.basename(filename), anchor='n',
                                        justify='center', width=90)
            def select_item(ev):
                canvas.select_from(id2, 0)
                canvas.select_to(id2, 'end')

                def delete_select(ev):
                    temp = []
                    for i in canvas.filenames:
                        if canvas.filenames[i] == filename:
                            temp.append(i)
                            canvas.delete(i)
                    for i in temp:
                        del canvas.filenames[i]
                canvas.bind("<Delete>", delete_select)

            canvas.tag_bind(id1, '<ButtonPress-1>', select_item)
            canvas.tag_bind(id2, '<ButtonPress-1>', select_item)
            canvas.filenames[id1] = filename
            canvas.filenames[id2] = filename
            if canvas.nextcoords[0] > 450:
                canvas.nextcoords = [50, canvas.nextcoords[1] + 80]
                region = canvas.bbox(ALL)
                canvas.configure(scrollregion=(0,0,0,region[-1]+80))
            else:
                canvas.nextcoords = [canvas.nextcoords[0] + 100, canvas.nextcoords[1]]

    # drop methods

    def drop_enter(event):
        event.widget.focus_force()
        #print('Entering %s' % event.widget)
        return event.action

    def drop_position(event):
        return event.action

    def drop_leave(event):
        #print('Leaving %s' % event.widget)
        return event.action

    def drop(event):
        if canvas.dragging:
            # the canvas itself is the drag source
            return REFUSE_DROP
        if event.data:
            files = canvas.tk.splitlist(event.data)
            for f in files:
                add_file(f)
        return event.action

    canvas.drop_target_register(DND_FILES)
    canvas.dnd_bind('<<DropEnter>>', drop_enter)
    canvas.dnd_bind('<<DropPosition>>', drop_position)
    canvas.dnd_bind('<<DropLeave>>', drop_leave)
    canvas.dnd_bind('<<Drop>>', drop)

    # drag methods

    def drag_init(event):
        data = ()
        sel = canvas.select_item()
        if sel:
            # in a decent application we should check here if the mouse
            # actually hit an item, but for now we will stick with this
            data = (canvas.filenames[sel],)
            canvas.dragging = True
            return ((ASK, COPY), (DND_FILES, DND_TEXT), data)
        else:
            # don't start a dnd-operation when nothing is selected; the
            # return "break" here is only cosmetical, return "foobar" would
            # probably do the same
            return 'break'

    def drag_end(event):
        # reset the "dragging" flag to enable drops again
        canvas.dragging = False

    canvas.drag_source_register(1, DND_FILES)
    canvas.dnd_bind('<<DragInitCmd>>', drag_init)
    canvas.dnd_bind('<<DragEndCmd>>', drag_end)

    def on_closing():
        global temp
        temp = None
        root.quit()

    root.update_idletasks()
    root.deiconify()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

    return temp



#files = Drag_and_drop("Выбор файлов", "Перетащите сюда ваши файлы:", "D:\\Python\\Chrome plugins\\Sublime Text.ico", True)
#files = Drag_and_drop("Выбор файлов", "Перетащите сюда ваши файлы:", sort=True)
files = Drag_and_drop("Выбор файлов", "Перетащите сюда файлы:")
if files:
    print(files)
