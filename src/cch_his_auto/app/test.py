def run():
    from cch_his_auto.app import PROFILE_PATH
    from cch_his_auto.driver import Driver
    from cch_his_auto.tasks.auth import login
    from cch_his_auto.tasks import danhsachnguoibenhnoitru
    from cch_his_auto.tasks.common import choose_dept
    from cch_his_auto.tasks.chitietnguoibenhnoitru import get_signature

    driver = Driver(profile_path=PROFILE_PATH)
    login(driver, "thanh.vuong", "96700840aB;")
    driver.goto(danhsachnguoibenhnoitru.URL)
    choose_dept(driver, "Khoa Ngoại thần kinh")
    danhsachnguoibenhnoitru.goto_patient(driver, 2412271409)
    print(get_signature(driver))

    driver.quit()

if __name__ == "__main__":
    run()
