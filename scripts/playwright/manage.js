const { chromium } = require('playwright-chromium');

(async () => {
    const browser = await chromium.launch();
    const context = await browser.newContext();
    const page = await context.newPage();

    await page.goto('http://raspberrypi.local/admin/index.php?login');

    // 登录
    await page.type('#loginpw', process.env.PIHOLEPASSWORD);
    await page.click('.btn.form-control');

    // 进入黑名单配置页面
    await page.click('a[href="groups-domains.php?type=black"]');

    // 添加
    await page.type('#new_domain', 'www.black.com')
    await page.type('#new_domain_comment', 'this is an invalid black domain for testing.')
    await page.click('#add2black')
    await page.click('[role="alert"] button')

    // 进入白名单配置页面
    await page.click('a[href="groups-domains.php?type=white"]');

    // 添加
    await page.type('#new_domain', 'www.white.com')
    await page.type('#new_domain_comment', 'this is an invalid white domain for testing.')
    await page.click('#add2white')
    await page.click('[role="alert"] button')

    // 删除黑名单
    await page.click('a[href="groups-domains.php?type=black"]');
    await page.click('#domainsTable tbody tr td button')
    await page.click('[role="alert"] button')

    // 删除白名单
    await page.click('a[href="groups-domains.php?type=white"]');
    await page.click('#domainsTable tbody tr td button')
    await page.click('[role="alert"] button')

    // 登出
    await page.click('a[href="?logout"]')

    await browser.close();
})();