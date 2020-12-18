import eel
import traceback

if __name__ == '__main__':

    eel.init("GUI/web")

    def my_other_thread():
        while True:
            print("I'm a thread")
            eel.sleep(1.0)                  # Use eel.sleep(), not time.sleep()

    eel.spawn(my_other_thread)

    eel.start('html/Start.html',block=False,size=(640,320))

    while True:
        print("I'm a main loop")
        eel.sleep(1.0)
    # while(i<10000):
    #     eel.sleep(0.01)
    #     print(i)
    #     i+=1
    traceback.print_exc()
