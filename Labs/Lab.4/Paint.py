#Canvas class from lecture
class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, w, **kargs):
        for i in range(x,x+w):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, h, **kargs):
        for i in range(y,y+h):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (y2-y1) / (x2-x1)
        for y in range(y1,y2):
            x= int(slope * y)
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))

#Start of my code

import numpy as np

class shape:
    def __init__(self,x,y):
        self.__x=x
        self.__y=y

    #virtual methods
    def x_coord(self):
        raise NotImplementedError
    def y_coord(self):
        raise NotImplementedError    
    
    def area(self):
        raise NotImplementedError
        
    def perimeter(self):
        raise NotImplementedError
    
    #method to check if objects overlap
    def overlap(self,object):
        shape1=self.para16()
        shape2=object.para16()

        #default answer False
        answer=False
        for i in range(16):
            for j in range(16):
                if shape1[i]==shape2[j]:
                    answer=True
        
        return answer

class rectangle(shape):
    def __init__(self,x,y,l,w):
        shape.__init__(self,x,y)
        self.__l=l
        self.__w=w

    #accessors
    def length(self):
        return self.__l

    def width(self):
        return self.__w

    def x_coord(self):
        return self.__x

    def y_coord(self):
        return self.__y

    #method to compute area
    def area(self):
        a=self.__l*self.__w
        return a

    #method to compute perimeter
    def perimeter(self):
        p=2*(self.__l+self.__w)
        return p
    
    #method to check if coordinates are within object
    #(x,y) is bottom left corner of rectange
    def inside(self,xcoord,ycoord):
        x_min=self.__x
        y_min=self.__y
        x_max=self.__x+self.__w
        y_max=self.__y+self.__l

        if (xcoord>=x_min and xcoord<=x_max) and (ycoord<=y_min and xcoord<=y_max):
            return True
        else:
            return False
        
    #method to return 16 (x,y) points on parameter
    def para16(self):
        #empty list to hold x/y coordinates; zip later to get pairs
        xlist=[]
        ylist=[]

        #min/max values for edges
        x_min=self.__x
        y_min=self.__y
        x_max=self.__x+self.__w
        y_max=self.__y+self.__l

        #generate random numbers
        count=0
        while count<16:
            xrand=np.random.uniform(x_min,x_max,1)
            yrand=np.random.uniform(y_min,y_max,1)

            #check if it falls on parameter of rectangle
            if xrand[0]==x_min or xrand[0]==x_max or yrand[0]==y_min or yrand[0]==y_max:
                xlist.append(xrand[0])
                ylist.append(yrand[0])
                count+=1
        
        #zip list of coordinates
        pairs=zip(xlist,ylist)
        return pairs

    def paint(self,canvas):
        canvas.v_line(self.__x, self.__y, self.__w)
        canvas.v_line(self.__x, self.__y + self.__l, self.__w)
        canvas.h_line(self.__x, self.__y, self.__l)
        canvas.h_line(self.__x + self.__w, self.__y, self.__l)

class circle(shape):
    def __init__(self,x,y,r):
        shape.__init__(self,x,y)
        self.__r=r

    #accessors
    def radius(self):
        return self.__r

    def x_coord(self):
        return self.__x

    def y_coord(self):
        return self.__y

    #area function
    def area(self):
        a=3.14*(self.__r**2)
        return a

    #perimeter (circumference) function
    def perimeter(self):
        p=2*3.14*self.__r
        return p
    
    #method to check if coordinates are within object
    #(x,y) is the center of the circle
    def inside(self,xcoord,ycoord):
        if ((xcoord-self.__x)**2 + (ycoord-self.__y)**2 <=self.__r**2):
            return True
        else:
            return False
    
    #method to return 16 (x,y) points on parameter
    def para16(self):
        #empty list to hold x/y coordinates; zip later to get pairs
        xlist=[]
        ylist=[]

        #min/max values
        x_min=self.__x-self.__r
        x_max=self.__x+self.__r
        y_min=self.__y-self.__r
        y_max=self.__y+self.__r

        #generate random numbers
        count=0
        while count<16:
            xrand=np.random.uniform(x_min,x_max,1)
            yrand=np.random.uniform(y_min,y_max,1)

            #check if it falls on parameter of circle
            if (xrand[0]-self.__x)**2 + (yrand[0]-self.__y)**2==self.__r**2:
                xlist.append(xrand[0])
                ylist.append(yrand[0])
                count+=1
        
        #zip list of coordinates
        pairs=zip(xlist,ylist)
        return pairs

    def paint(self,canvas):
        coords=self.para16()
        xy=[list(_) for _ in zip(*coords)]

        for i in range(15):
            canvas.line(xy[0][i],xy[1][i],xy[0][i+1],xy[1][i+1])
        canvas.line(xy[0][15],xy[1][15],xy[0][0],xy[1][0])

class triangle(shape):
    def __init__(self,x,y,h,b,sides): #where sides is a list of the 3 sides of the triangle
        shape.__init__(self,x,y)
        self.__h=h
        self.__b=b
        self.__sides=sides

    #accessors
    def height(self):
        return self.__h

    def base(self):
        return self.__b
    
    def sides(self):
        return self.__sides

    def x_coord(self):
        return self.__x

    def y_coord(self):
        return self.__y
    
    #area function
    def area(self):
        a=self.__h*self.__b/2
        return a

    #perimeter function
    def perimeter(self):
        p=sum(self.__sides)
        return p
    
    #method to check if coordinates are within object
    #(x,y) is the bottom left corner of the triangle
    def inside(self,xcoord,ycoord):
        #coordinates of top corner and bottom right corner of triangle
        topx=self.__x+(self.__b/2)
        topy=self.__y+self.__h
        rightx=self.__x+self.__b
        righty=self.__y

        A=triangle.area(self)

        #finding area of triangle: left,top,input coords
        LTI=(1/2)*abs((self.__x*(topy-ycoord))+(topx*(ycoord-self.__y)+(xcoord*(self.__y-topy))))

        #finding area of triangle: top,right,input coords
        TRI=(1/2)*abs((topx*(righty-ycoord))+(rightx*(ycoord-topy)+(xcoord*(topy-righty))))

        #finding area of triangle: left,right,input coords
        LRI=(1/2)*abs((self.__x*(righty-ycoord))+(rightx*(ycoord-self.__y)+(xcoord*(self.__y-righty))))

        if LTI+TRI+LRI==A:
            return True
        else:
            False

    #method to return 16 (x,y) points on parameter
    def para16(self):
        #empty list to hold x/y coordinates; zip later to get pairs
        xlist=[]
        ylist=[]

        #min/max values
        x_min=self.__x
        x_max=self.__x+self.__b
        y_min=self.__y
        y_max=self.__y+self.__h
        topx=self.__x+(self.__b/2)

        #generate random numbers
        count=0
        while count<16:
            xrand=np.random.uniform(x_min,x_max,1)
            yrand=np.random.uniform(y_min,y_max,1)

            #check if it falls on parameter of circle
            if yrand[0]==y_min or (xrand==topx and yrand==y_max):
                xlist.append(xrand[0])
                ylist.append(yrand[0])
                count+=1
        
        #zip list of coordinates
        pairs=zip(xlist,ylist)
        return pairs

    def paint(self,canvas):
        canvas.h_line(self.__x,self.__y,self.__b)
        canvas.line(self.__x,self.__y,self.__x+(self.__b/2),self.__y+self.__h)
        canvas.line(self.__x+(self.__b/2),self.__y+self.__h,self.__x+self.__b,self.__y)

#CompoundShape class from lecture
class CompoundShape(shape):
    def __init__(self, shapes):
        self.shapes = shapes

    def paint(self, canvas):
        for s in self.shapes:
            s.paint(canvas)