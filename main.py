import cv2
import os, sys
import pyautogui
import multiprocessing
import time
import re

# python3 <script>.py <fullpath\to\kkrieger> -o <fullpath\to\output>
# Ex: python3 main.py 'home/alexey/Загрузки/pno0001.exe' -o 'home/alexey/PycharmProjects/testing_kkrieger/output'

_, path_to_app, _, path_to_output = sys.argv
os.system(f'mkdir {path_to_output}/screenshots {path_to_output}/fps_log')
os.system(f'touch {path_to_output}/fps_log/average_fps.txt')
HEIGTH = pyautogui.size().height
WIDTH = pyautogui.size().width

def run():
    # Стандартный запуск wine без виртуального стола с выставленным разрешением экрана после выполнения скрипта \\
    # ломает разрешение, по крайней мере на linux системах, поэтому был выбран такой путь запуска.
    os.system(f'WINEDEBUG=+fps wine explorer /desktop=kkrieger,{WIDTH}x{HEIGTH} {path_to_app} 2>&1 | tee /dev/stderr | sed -u -n -e "/trace/ s/.*approx //p" > {path_to_output}/fps_log/fps_log.txt')

def can_we_start():
    time.sleep(6)
    switch_1()
    pyautogui.press('enter', presses=2)
    time.sleep(1)
    main_scene = pyautogui.screenshot(region=(0, 0, WIDTH, HEIGTH))
    main_scene.save(f'{path_to_output}/screenshots/start_main_scene.png') # Скриншот как игра загрузилась на сцену
    pyautogui.keyDown('w')
    switch_2()
    pyautogui.keyUp('w')
    # Скриншот в конце теста
    os.replace(f'{path_to_output}/screenshots/screenshot.png', f'{path_to_output}/screenshots/end_main_scene.png')
    os.system('wineserver -k')
    avg = avg_fps()
    with open(f'{path_to_output}/fps_log/average_fps.txt', 'w') as file:
        file.write(str(avg)+' fps')


def do_screenshot(standart):
    screenshot = pyautogui.screenshot(region=(0, 0, WIDTH, HEIGTH))
    screenshot.save(f'{path_to_output}/screenshots/screenshot.png')
    screenshot = cv2.imread(f'{path_to_output}/screenshots/screenshot.png')

    """ Check for similarities between the 2 imgs """
    orb = cv2.ORB_create()
    kp_1, desc_1 = orb.detectAndCompute(standart, None)
    kp_2, desc_2 = orb.detectAndCompute(screenshot, None)

    matcher = cv2.BFMatcher()
    matches = matcher.knnMatch(desc_1, desc_2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])
    return len(good)

def switch_1():
    standart = pyautogui.screenshot(region=(0, 0, WIDTH, HEIGTH))
    standart.save(f'{path_to_output}/screenshots/standart.png')
    standart = cv2.imread(f'{path_to_output}/screenshots/standart.png')
    while True:
        number_of_difference = do_screenshot(standart)
        if number_of_difference < 350:
            print('difference, number of difference is', number_of_difference)
            return

def switch_2():
    while True:
        standart = pyautogui.screenshot(region=(0, 0, WIDTH, HEIGTH))
        standart.save(f'{path_to_output}/screenshots/standart.png')
        standart = cv2.imread(f'{path_to_output}/screenshots/standart.png')
        number_of_difference = do_screenshot(standart)
        if number_of_difference > 140:
            print('same, number of difference is', number_of_difference)
            return

def avg_fps():
    with open(f'{path_to_output}/fps_log/fps_log.txt', 'r') as file:
        fps_sum, n = 0, 0
        for line in file:
            line = re.split('f', f'{line.rstrip()}')
            fps = float(line[0])
            if fps > 3:
                n += 1
                fps_sum += fps
    if n > 0:
        return "%.2f" % (fps_sum / n)

if __name__ == '__main__':
    run_wine = multiprocessing.Process(target=run)
    run_wine.daemon = True
    run_wine.start()
    if run_wine.is_alive():
        good_matches = multiprocessing.Process(target=can_we_start)
        good_matches.start()
