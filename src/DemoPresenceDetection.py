import face_recognition
import time
import threading
import cv2
import vlc
import pickle
import datetime
from gtts import gTTS

# import asyncio
# import websockets
import socket

#port = 1337
#s = socket.socket()
# host = socket.gethostname()
#host = 'localhost'
#s.bind((host, port))
#s.listen(15)

host = 'localhost'
port = 1337

cap = cv2.VideoCapture(0)

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()
sound = "sound.mp3"

filename = "mypic.png"

enc = "encodings/room403.pickle"

# clients for output on script
clients = list()
# nclients to send on server
nclients = list()

def cameraon():
    while cap.isOpened():
        ret, frame = cap.read()
        # cv2.imshow('frame', frame)
        if ret:
            # frame = cv2.flip(frame, 0)

            # write the flipped frame
            # out.write(frame)

            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Release everything if job is finished
    cap.release()
    # out.release()
    cv2.destroyAllWindows()


def save_and_play(str):
    tts = gTTS(str)
    tts.save(sound)

    # play
    media = vlc_instance.media_new(sound)
    player.set_media(media)
    player.play()
    time.sleep(1)
    duration = player.get_length() / 1000
    print(duration)
    time.sleep(duration)


def ssend(client, filename, nclients):
    s = socket.socket()
    # host = socket.gethostname()
    s.connect((host, port))
    client = client + "|"
    s.send(client.encode("utf-8"))

    # clsend = str()
    # for i in range(len(nclients)):
    #     clsend = clsend + nclients[i] + "\n"
    # s.send(clsend.encode("utf-8"))

    f = open(filename, 'rb')
    l = f.read(1024)
    while (l):
        s.send(l)
        # print('Sent ',repr(l))
        l = f.read(1024)
    f.close()


    # f.close()
    print('Successfully send the file')
    s.close()
    # print('connection closed')


async def asend(loop):
    task = loop.create_task(asend(client))
    # remaining_work_not_depends_on_foo()
    loop.run_until_complete(task)
    async with websockets.connect(
            'ws://localhost:1337') as websocket:
        # name = input("What's your name? ")
        # name = "123 456 789 ,.:a;sdl;adl;2[d;"
        # print(name)

        await websocket.send(name)
        # print(f"> {name}")


def identify(name, frame):
    now = datetime.datetime.now()
    now1 = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    # now.year, now.month, now.day, now.hour, now.minute, now.second
    # name = name + " " + now.hour + now.minute + now.second
    client = name + " " + now1
    print(client)

    nowf = str(now.day) + "." + str(now.month) + "." + str(now.year) \
           + "." + str(now.hour) + "." + str(now.minute) + "." + str(now.second)
    savefile = "captures-new/" + str(nowf) + "_" + name + ".png"
    print(savefile)
    cv2.imwrite(savefile, frame)

    if name == "Unknown":
        print("Unknown person")

    elif name in clients:
        # nclients.remove(client)
        clients.remove(name)
        temp = "Goodbye, " + name
        print(temp)
        # save_and_play(temp)
        print("Users:", clients.__len__(), ". List of users: ", clients)
    else:
        # nclients.append(client)
        clients.append(name)
        temp = "Hello, " + name
        print(temp)
        # save_and_play(temp)
        print("Users:", clients.__len__(), ". List of users: ", clients)

    ssend(client, savefile, nclients)


def waiting():
    print("waiting statement")


def starting():
    print('starting')

    data = pickle.loads(open(enc, "rb").read())
    cur_time = time.time()
    residual_time = time.time()
    while True:
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        cv2.imwrite(filename, rgb)
        r = frame.shape[1] / float(rgb.shape[1])

        image = face_recognition.load_image_file(filename)
        face_locations = face_recognition.face_locations(image)
        boxes = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []
        matchedIdxs = []
        counts = {}

        # # # # #
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                # counts = {}

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # update the list of names
            names.append(name)

            print(datetime.datetime.now(), "Boxes: ", boxes, ". Names:", names, ". Count:", names.__len__())


def act():
    print('act')

    data = pickle.loads(open(enc, "rb").read())
    # while True:
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    cv2.imwrite(filename, rgb)
    # cv2.imwrite("captures/" + filename, rgb)
    r = frame.shape[1] / float(rgb.shape[1])

    image = face_recognition.load_image_file(filename)
    face_locations = face_recognition.face_locations(image)
    boxes = face_recognition.face_locations(rgb)
    encodings = face_recognition.face_encodings(rgb, boxes)
    name = "Unknown"
    names = []
    matchedIdxs = []
    counts = {}

    # # # # #
    for encoding in encodings:
        # attempt to match each face in the input image to our known
        # encodings
        matches = face_recognition.compare_faces(data["encodings"],
                                                 encoding)
        name = "Unknown"

        # check to see if we have found a match
        if True in matches:
            # find the indexes of all matched faces then initialize a
            # dictionary to count the total number of times each face
            # was matched
            matchedIdxs = [i for (i, b) in enumerate(matches) if b]
            # counts = {}

            # loop over the matched indexes and maintain a count for
            # each recognized face face
            for i in matchedIdxs:
                name = data["names"][i]
                counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

            # update the list of names
        names.append(name)

        print(datetime.datetime.now(), "Boxes: ", boxes, ". Names:", names, ". Count:", names.__len__())

    identify(name, frame)


def listing():
    print("listing: ", clients)



def __init__():
    # main components that don't need to be reinitialized
    print("init...")
    clients = list()
    # demo_encode.abc()


def main():
    # waiting()
    while True:
        try:
            inputstr = input()

            # 1: Input to face_rec
            if inputstr == "waiting": waiting()
            if inputstr == "starting": starting()
            if inputstr == "1": act()
            if inputstr == "listing": listing()

        except ValueError:
            print("Sorry, wrong command")
            continue


if __name__ == "__main__":
    __init__()
    mainfunc = threading.Thread(target=main)
    videostream = threading.Thread(target=cameraon)

    # mainfunc = multiprocessing.Process(target=main)
    # videostream = multiprocessing.Process(target=cameraon)

    mainfunc.start()
    videostream.start()
    # mainfunc.join()
    # videostream.join()

# loop over the recognized faces
# for ((top, right, bottom, left), name) in zip(boxes, names):
#    # rescale the face coordinates
#    top = int(top * r)
#    right = int(right * r)
#    bottom = int(bottom * r)
#    left = int(left * r)

    # draw the predicted face name on the image
#    cv2.rectangle(frame, (left, top), (right, bottom),
#                  (0, 255, 0), 2)
#    y = top - 15 if top - 15 > 15 else top + 15
#    cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
#                0.75, (0, 255, 0), 2)

    # loop over the matched indexes and maintain a count for
    # each recognized face face

#    for i in matchedIdxs:
#        name = data["names"][i]
#        counts[name] = counts.get(name, 0) + 1

    # determine the recognized face with the largest number
    # of votes (note: in the event of an unlikely tie Python
    # will select first entry in the dictionary)
    # name = max(counts, key=counts.get)

    # # # # #
#else:
    # print(datetime.datetime.now(), "Unknown person")
#    continue
    # print("Unknown person")
    # print("Unknown")