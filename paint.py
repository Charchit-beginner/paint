from tkinter import *
from tkinter.colorchooser import askcolor
from PIL import Image
from PIL import ImageTk
from tkinter.filedialog import asksaveasfilename, askopenfilename

class gui(Tk):
    def __init__(self):
        super().__init__()
        self.w,self.h = 700,600
        self.title("paint")
        self.buttonchose = "circle"
        self.stack = []
        self.stackRedo = []
        self.paint_color = "black"
        self.eraser = False
        self.i = 0
        self.penSize = Scale(self,from_=0,to=30,orient="horizontal",)
        self.penSize.set(3)
        self.penSize.grid(row=0,column=1)

        
        Button(self,text="Eraser",command=self.Eraser).grid(row=0,column=2)
        Button(self,text="Cleat All",command=self.clearAll).grid(row=0,column=3)
        Button(self,text="Pen",command=self.pen).grid(row=0,column=4)
        Button(self,text="Choose Color",command=self.color).grid(row=0,column=5)
        Button(self,text="line",command=self.line).grid(row=0,column=6)
        Button(self,text="straightline",command=self.straightline).grid(row=0,column=7)
        Button(self,text="Rect",command=self.recta).grid(row=0,column=8)
        Button(self,text="circle",command=self.circle).grid(row=0,column=9)
        Button(self,text="undo",command=self.undo).grid(row=0,column=10)
        Button(self,text="redo",command=self.redo).grid(row=0,column=11)
        Button(self,text="changebgcolor",command=self.changeBackground).grid(row=0,column=12)
        
        Button(self,text="Save",command=self.save).grid(row=0,column=13)
        Button(self,text="open",command=self.open).grid(row=0,column=14)
        self.canvas = Canvas(self,width=self.w,height=self.h,bg="white")
        self.canvas.grid(row=1,columnspan=15)

        self.canvas.bind("<B1-Motion>",self.paint)
        self.canvas.bind("<ButtonRelease-1>",self.release)
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        
        self.oldposx,self.oldposy = None,None
        self.mainloop()

    def changeBackground(self):
        paint_color = askcolor()[1]

        # self.canvas.config(bg=paint_color)
        self.canvas.create_rectangle(-1,-2,self.w+5,self.h+5,fill=paint_color)
    
    
    def undo(self):
        # x = self.stack.pop()
        # self.stackRedo.append(x)
        # self.canvas.delete(x)
        # self.canvas.create_oval(x)
        self.canvas.itemconfig(self.stack[-1],state="hidden")
        self.stackRedo.append(self.stack[-1])
        self.stack.pop()
        print(self.stack)
        # if self.i > 1: 
        #     self.i -= 1
    
    def save(self):
        self.canvas.update()
        self.canvas.postscript(file="circles.eps")
        img = Image.open("circles.eps")
        img.save("circles.png", "png")
    def open(self):
        filename = askopenfilename( filetypes =[('PNG file', '*.png'),("JPG file","*.txt"),("All Files","*")])

        img = Image.open(filename)
        img = img.resize((self.w, self.h),Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(img)
        self.canvas.create_image(1,1,image=self.img,anchor="nw")
       
        
    def redo(self):
        # y = self.stackRedo.pop()
        # self.stack.append(y)
        # print(self.stack)
        # self.canvas.create_oval()
        self.canvas.itemconfig(self.stackRedo[-1],state="normal")
        self.stack.append(self.stackRedo[-1])
        self.stackRedo.pop(-1)
        print(self.stackRedo)
        # if self.a  > self.i:
        #     self.i += 1
    def Eraser(self):
        self.buttonchooser("line")
        self.eraser = True
        self.penSize.set(30)
    def clearAll(self):
        self.canvas.delete("all")
    def pen(self):
        pass
    def color(self):
        self.paint_color = askcolor()[1]
    def buttonchooser(self,button,eraserMode = False):
        self.buttonchose = button
        self.eraser = eraserMode
        return button
    def line(self):
        self.canvas.configure(cursor="pencil")
        self.buttonchooser("line")
    def recta(self):
        self.buttonchooser("rect")
    def circle(self):
        self.buttonchooser("circle")
    def straightline(self):
        self.canvas.configure(cursor="pencil")
        self.buttonchooser("straightline")

    

    def on_button_press(self,event):
        self.i+=1
        self.a = self.i
        self.color = "white" if self.eraser else self.paint_color
        self.start_x , self.start_y = event.x,event.y
        if self.buttonchose == "straightline":
            self.line = self.canvas.create_line(-122,-122,-123,-123,fill=self.color,
                        tags=f"rect{self.i}",width=self.penSize.get(),capstyle=ROUND, smooth=TRUE, splinesteps=36)
            # self.stack.append(self.line)
        elif self.buttonchose == "rect":
            self.rect = self.canvas.create_rectangle(-122, -122, -123,-123 ,fill=self.paint_color,width=5,tags=f"rect{self.i}")
            # self.stack.append(self.rect)
           
        elif self.buttonchose == "circle":
            self.circle = self.canvas.create_oval(-122,-122,-123,-123,fill = self.color,tags=f"rect{self.i}")
            # self.stack.append(self.circle)
        self.stack.append(f"rect{self.i}")
        
        


    def paint(self,event):
        self.color = "white" if self.eraser else self.paint_color

        if self.buttonchose == "line":
            
            if self.oldposx and self.oldposy:
                
                line = self.canvas.create_line(self.oldposx,self.oldposy,event.x,event.y,\
                    fill=self.color,width=self.penSize.get(),capstyle=ROUND, smooth=TRUE, splinesteps=36,tag=f"rect{self.i}")
                self.stack.pop()
                self.stack.append(f"rect{self.i}")
                
            
            self.oldposx,self.oldposy = event.x,event.y
        elif self.buttonchose == "rect":
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
        elif self.buttonchose == "circle":
            self.canvas.coords(self.circle,self.start_x,self.start_y,event.x,event.y)
            
        elif self.buttonchose == "straightline":
            self.canvas.coords(self.line,self.start_x,self.start_y,event.x,event.y)
            

    def release(self,event):
        # self.canvas.delete('temp_rect_objects')
        # self.canvas.delete('temp_line_objects')
        # self.canvas.delete('temp_circle_objects')
        
        self.oldposx,self.oldposy = None,None

if __name__ == '__main__':
    win =  gui()



    