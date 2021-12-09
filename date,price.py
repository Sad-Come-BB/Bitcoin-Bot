#file_object  = open("everything.txt", "r")

with open('everything.txt' , 'r') as f:
#    f_contents = f.read(50)
  #  print (f_contents, end = ' ' )
    #n = 2
    #f_contents = f.read(77*n)
    #print (f_contents, end = ' ' )
    f_contents = f.readline()
    print (f_contents)
    f_contents = f.readline()
    print (f_contents)
    for i in range (1):
        f_contents = f.readline()
        y1 = f_contents[13:22]
        y2 = f_contents[53:63]
        print (y1)
        print (y2)

#string = "freeCodeCamp"
#print(string[0:5])