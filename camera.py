# import the opencv library
import cv2
import matplotlib.pyplot as plt


# define a video capture object
vid = cv2.VideoCapture(0)


fig = plt.figure()
ax = fig.add_subplot(1,1,1)


def animate():
    ax.clear()
    x = []
    y = []

oneFrame = True

while (True):
    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)
    # print(frame)
    # print("abrakadabra")

    if oneFrame:
        controlFrame = frame
        # for each in frame:
        #     # print(each, "tu som")
        #     for eache in each:
        #         print(eache, "aj ja som")
        oneFrame = False

    red = frame[:,:,0][0]


    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()

plt.show()

maximus = 0
size = 0
for each in controlFrame:
    x = []
    size = len(each)
    for eache in each:
        # print(eache)
        # x.append(eache[0])
        # print(x)
        maximus = max(maximus, max(eache))

print(controlFrame)
blue = controlFrame[:,:,0]
print(blue)
print(len(blue[0]))
yos = blue[0]
xos = list(range(0, len(blue[0])))
print(maximus, size, len(frame))
# print(len(x))
x1 = [1, 2, 3]
y1 = [2, 4, 1]

# plt.plot(xos, yos)
# # plt.plot(x1, y1)
# # naming the x axis
# plt.xlabel('x - axis')
# # naming the y axis
# plt.ylabel('y - axis')
#
# # giving a title to my graph
# plt.title('My first graph!')
#
# # function to show the plot
# plt.show()

