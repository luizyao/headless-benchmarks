import asyncio
import os

from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("http://raspberrypi.local/admin/index.php?login")

        # 输入密码
        await page.type("#loginpw", os.getenv("PIHOLEPASSWORD"))

        # 登录
        await page.click(".btn.form-control")

        # 登出
        await page.click('a[href="?logout"]')

        await browser.close()


asyncio.run(main())
