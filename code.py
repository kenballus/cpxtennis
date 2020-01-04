from random import randint
from time import sleep
from adafruit_circuitplayground.express import cpx

def gameloop():
    """ The mainloop. """

    print("Starting a new game!")

    score = [0, 0]

    # Set up a new point:
    while True:
        clear_pixels()
        print("NEW POINT")
        play_score(score)

        curr_pixel = randint(4, 5)
        prev_pixel = -1
        pixel_direction = -((curr_pixel - 4) * 2 - 1)

        delay = .35

        a_held = False
        b_held = False

        # The point:
        while True:
            button_a = cpx.button_a
            button_b = cpx.button_b

            # Check for moves
            if button_a and not a_held:
                a_held = True
                if curr_pixel < 5:
                    if pixel_direction == -1:
                        cpx.play_file("sound/plip.wav")
                        sleep(delay)
                        pixel_direction *= -1

                        if delay > .01:
                            delay /= 1.3
                    
                else:
                    if score_point(1, score):
                        return
                    break
                    

            if not button_a and a_held:
                a_held = False

            if button_b and not b_held:
                b_held = True
                if curr_pixel > 4:
                    if pixel_direction == 1:
                        cpx.play_file("sound/plop.wav")
                        sleep(delay)
                        pixel_direction *= -1

                        if delay > .01:
                            delay /= 1.3
                    
                else:
                    if score_point(0, score):
                        return
                    break
                    

            if not button_b and b_held:
                b_held = False

            # Update pixel trackers
            prev_pixel = curr_pixel
            curr_pixel += pixel_direction

            # Check for slow losers
            if curr_pixel == 10:
                if score_point(0, score):
                    return
                break
                
            elif curr_pixel == -1:
                if score_point(1, score):
                    return
                break

            # Write to pixels
            if prev_pixel != -1:
                cpx.pixels[prev_pixel] = (0, 0, 0)
            cpx.pixels[curr_pixel] = (30, 0, 30)

            sleep(delay)

def play_score(score):
    if score[0] == 0:
        cpx.play_file("sound/love.wav")
    elif score[0] == 1:
        cpx.play_file("sound/fifteen.wav")
    elif score[0] == 2:
        cpx.play_file("sound/thirty.wav")
    elif score[0] == 3 and score[1] < 3:
        cpx.play_file("sound/forty.wav")

    if score[0] < 3 and score[1] == score[0]:
        cpx.play_file("sound/all.wav")
        return

    if score[1] == 0:
        cpx.play_file("sound/love.wav")
    elif score[1] == 1:
        cpx.play_file("sound/fifteen.wav")
    elif score[1] == 2:
        cpx.play_file("sound/thirty.wav")
    elif score[1] == 3 and score[0] < 3:
        cpx.play_file("sound/forty.wav")

    elif score[0] == score[1] >= 3:
        cpx.play_file("sound/deuce.wav")

    elif (score[0] == score[1] + 1) and (score[1] >= 3):
        cpx.play_file("sound/ad_a.wav")
    elif (score[1] == score[0] + 1) and (score[0] >= 3):
        cpx.play_file("sound/ad_b.wav")

def score_point(player, score):
    score[player] += 1
    print("PLAYER", "AB"[player], "SCORED!")
    print("NEW SCORE:", score)

    if player - 1 == 0:
        flash_red(range(5))
    else:
        flash_red(range(5, 10))

    if score[player] >= 4 and score[player] - 1 > score[1 - player]:
        game_over(1 - player, score)
        return True

    wait_for_start()
    return False

def game_over(loser, score):
    print("Player", "AB"[1 - loser], "won", score[0], "to", str(score[1]) + ".")
    clear_pixels()

    if loser == 0:
        rainbow(range(5, 10))

    elif loser == 1:
        rainbow(range(5))

def clear_pixels(spread=range(10)):
    """ Turns off all pixels """

    for i in spread:
        cpx.pixels[i] = (0, 0, 0)

def flash_red(pixels):
    """ Flashes the given pixels red. Also plays a sound. """

    clear_pixels()

    cpx.play_file("sound/bamp.wav")

    for _ in range(10):
        for i in pixels:
            cpx.pixels[i] = (50, 0, 0)
        sleep(.05)
        for i in pixels:
            cpx.pixels[i] = (0, 0, 0)
        sleep(.05)

def rainbow(pixels):
    """ Cycles the given pixels through the rainbow and back. Also plays a sound. """

    cpx.play_file("sound/tada.wav")
    r, g, b = (30, 0, 0)

    for _ in range(75):
        for i in pixels:
            cpx.pixels[i] = (r, g, b)
    
        if r > 0 and b == 0:
            r -= 1
            g += 1
        if g > 0 and r == 0:
            g -= 1
            b += 1
        if b > 0 and g == 0 and r < 29:
            b -= 1
            r += 1
        sleep(.005)

    for _ in range(75):
        for i in pixels:
            cpx.pixels[i] = (r, g, b)

        if r > 0 and g == 0:
            r -= 1
            b += 1
        if b > 0 and r == 0:
            b -= 1
            g += 1
        if g > 0 and b == 0:
            g -= 1
            r += 1
        sleep(.005)

    clear_pixels()

def half_color(half, color):
    if half == "A":
        for i in range(5):
            cpx.pixels[i] = color
    elif half == "B":
        for i in range(5, 10):
            cpx.pixels[i] = color

def wait_for_start():
    """ The game starts when both players press their buttons simulataneously, then both release. """

    a_pressed = False
    b_pressed = False

    while True:
        if cpx.button_a:
            half_color("A", (0, 30, 0))
            a_pressed = True

        if cpx.button_b:
            half_color("B", (0, 30, 0))
            b_pressed = True

        if a_pressed and b_pressed:
            while True:
                if not cpx.button_a and not cpx.button_b:
                    return

def main():
    while True:
        wait_for_start()
        gameloop()

main()
