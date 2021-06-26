import add_parent_dir
import get_screen

if __name__ == "__main__":
    img = get_screen.catch_screen()
    oppo_num, mine_num = get_screen.count_minions(img)
    oppo_res, mine_res = get_screen.test_taunt(img, oppo_num, mine_num)
    print(f"Oppo's taunt minion: {oppo_res}")
    print(f"My taunt minion: {mine_res}")
    oppo_res, mine_res = get_screen.test_divine_shield()
    print(f"Oppo's divine shield minion: {oppo_res}")
    print(f"My divine shield minion: {mine_res}")
