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

        await page.click('a[href="groups-domains.php?type=black"]')
        await page.type("#new_domain", "www.black.com")
        await page.type(
            "#new_domain_comment", "this is an invalid black domain for testing."
        )
        await page.click("#add2black")
        await page.click('[role="alert"] button')

        # 进入白名单配置页面
        await page.click('a[href="groups-domains.php?type=white"]')

        # 添加
        await page.type("#new_domain", "www.white.com")
        await page.type(
            "#new_domain_comment", "this is an invalid white domain for testing."
        )
        await page.click("#add2white")
        await page.click('[role="alert"] button')

        # 删除黑名单
        await page.click('a[href="groups-domains.php?type=black"]')
        await page.click("#domainsTable tbody tr td button")
        await page.click('[role="alert"] button')

        # 删除白名单
        await page.click('a[href="groups-domains.php?type=white"]')
        await page.click("#domainsTable tbody tr td button")
        await page.click('[role="alert"] button')

        # 登出
        await page.click('a[href="?logout"]')

        await browser.close()


asyncio.run(main())
