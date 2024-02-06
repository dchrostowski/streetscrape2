import puppeteer from "puppeteer";
import fs from "fs";


const pullScore = async (page,text) => {

    const xpath = `//h2/a[contains(text(),"${text}")]/parent::h2/following-sibling::div/span[1]`
    try{
        await page.waitForXPath(xpath, {timeout: 500})
    }
    catch(err) {return '0'}

    const element = await page.$x(xpath)
    const elementText = await page.evaluate(el => el.textContent, element[0])
    console.log(elementText)
    if(elementText === '') return '0'
    return elementText.trim().replace("/10","")
}

(async () => {
    //const links = JSON.parse(await fs.readFileSync('../gurufocus_unscrapable.json'))
    if(process.argv.length !== 4) {
        console.error("invalid arguments.  provide url as first argument.")
        process.exit(1)
    }
    const link = process.argv[2]
    const symbol = process.argv[3]
    const browser = await puppeteer.launch()
    const page = await browser.newPage()

    try {
        const browser = await puppeteer.launch();
        const page = await browser.newPage();
        await page.setViewport({width: 1366, height: 768});
        await page.setUserAgent('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36');

        await page.goto(link, {waitUntil:'load',timeout: 10000})
        await page.waitForXPath('//div[contains(@class,"chart-section")][1]/div[1]/div[1]/span/span/div/a[1]/span[2]', {timeout: 3000})

        const elHandle = await page.$x('(//div[contains(@class,"chart-section")][1]/div[1]/div[1]/span/span/div/a[1]/span[2])', {timeout: 3000})
        const text = await page.evaluate(el => el.textContent, elHandle[0])
        console.log(`got score: ${text} `)
        const score = text.trim().replace('/100','')
        const balancesheetScore = await pullScore(page, "Financial Strength")
        const profitabilityScore = await pullScore(page, "Profitability Rank")
        const growthScore = await pullScore(page, "Growth Rank")
        const valueScore = await pullScore(page, "GF Value Rank")
        const momentumScore = await pullScore(page, "Momentum Rank")


        const priceEl = await page.$x('//div[@class="m-t-xs"]/span[1]')
        const priceText = await page.evaluate(el => el.textContent, priceEl[0])
        const price = priceText.trim().replace('$','').trim()

        console.log(`Data for ${symbol}:`)
        const item = {
            'symbol': symbol,
            'price_at_rating': price,
            'balancesheet': balancesheetScore,
            'profitability': profitabilityScore,
            'growth': growthScore,
            'value': valueScore,
            'momentum': momentumScore,
            'quant': score
        }


        console.log(item)
        fs.writeFileSync(`gurufocus_${symbol}.json`, JSON.stringify(item))

    }
    catch(err) {
        console.error(err)
    }

    finally {
        await page.close()
        await browser.close();
        process.exit(0)
    }

  })();

