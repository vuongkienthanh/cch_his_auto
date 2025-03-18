"""
### Tasks that operate on *In điều dưỡng*
### *Bảng kê chi phí BHYT*
###### inside "*Chi tiết người bệnh nội trú*
"""

import time

from cch_his_auto.tasks.chitietnguoibenhnoitru import indieuduong
from cch_his_auto.driver import Driver
from cch_his_auto.tasks.editor.sign_patient_name import sign_patient

def open(driver: Driver):
    indieuduong.goto(driver, "Bảng kê chi phí BHYT")

def close(driver: Driver):
    driver.find_all(".ant-modal button[aria-label='Close']")[1].click()

def goto_iframe(driver: Driver):
    iframe = driver.waiting(".ant-modal iframe")
    driver.switch_to.frame(iframe)

def goout_iframe(driver: Driver):
    driver.switch_to.parent_frame()

def sign_staff(driver: Driver):
    driver.clicking(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image button")
    driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(5) .sign-image img")

def sign_patient(driver: Driver, signature: str):
    driver.clicking(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image button")
    sign_patient(driver, signature)
    driver.waiting(".ant-row:nth-child(26) .ant-col:nth-child(4) .sign-image img")
