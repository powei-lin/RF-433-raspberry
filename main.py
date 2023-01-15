from time import perf_counter_ns
from datetime import datetime
import matplotlib.pyplot as pyplot
import RPi.GPIO as GPIO

RECEIVED_SIGNAL = [[], []]  # [[time of reading], [signal reading]]
MAX_DURATION = 2
RECEIVE_PIN = 4

if __name__ == '__main__':
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(RECEIVE_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    input("press enter to start")
    print('**Started recording**')
    time_delta = 0
    beginning_time = perf_counter_ns()
    prev_status = -1
    count = 0
    while time_delta < MAX_DURATION*1e9:
        time_delta = (perf_counter_ns() - beginning_time)
        current_status = GPIO.input(RECEIVE_PIN)
        if current_status is not prev_status:
            RECEIVED_SIGNAL[0].append(time_delta-1)
            RECEIVED_SIGNAL[1].append(prev_status)
            RECEIVED_SIGNAL[0].append(time_delta)
            RECEIVED_SIGNAL[1].append(current_status)
            prev_status = current_status
        count += 1
    print('**Ended recording**')
    print(len(RECEIVED_SIGNAL[0]), 'samples recorded')
    print("total request time:", count)
    GPIO.cleanup()

    print('**Processing results**')
    for i in range(len(RECEIVED_SIGNAL[0])):
        RECEIVED_SIGNAL[0][i] /= 1e9

    print('**Plotting results**')
    date_str = datetime.now().strftime('%Y_%m%d_%H%M')
    with open(f"data_{date_str}.csv", 'w') as ofile:
        ofile.write("x,y\n")
        for i, j in zip(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1]):
            ofile.write(f"{i},{j}\n")
    pyplot.plot(RECEIVED_SIGNAL[0], RECEIVED_SIGNAL[1])
    pyplot.axis([0, MAX_DURATION, -1, 2])
    pyplot.savefig("img.png")
    # pyplot.show()
