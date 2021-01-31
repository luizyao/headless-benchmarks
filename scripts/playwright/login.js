const { chromium } = require('playwright-chromium');

(async () => {
    const browser = await chromium.launch();
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('http://raspberrypi.local/admin/index.php?login');

    // 输入密码
    await page.type('#loginpw', process.env.PIHOLEPASSWORD);

    // 登录
    await page.click('.btn.form-control');

    // 登出
    await page.click('a[href="?logout"]');

    await browser.close();
})();