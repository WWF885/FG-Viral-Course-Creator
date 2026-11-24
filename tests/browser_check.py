from playwright.sync_api import sync_playwright
from pathlib import Path
r=Path(__file__).resolve().parents[1]; errors=[]
js=(r/'assets/visuals.js').read_text()
def load(page, path, src):
 html=(r/path).read_text(); page.set_content(html.replace(f'<script src="{src}"></script>', '<script>'+js+'</script>'))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=__import__('os').environ.get('CHROMIUM_PATH'),args=['--no-sandbox']); page=b.new_page(viewport={'width':1440,'height':900}); page.on('pageerror',lambda e:errors.append(str(e)))
 load(page,'assets/catalog.html','visuals.js'); assert page.locator('article').count()==26; assert page.locator('article svg').count()==26
 quiz=page.locator('article[data-type=quiz]'); quiz.get_by_role('button',name='收集').click(); assert '正确' in quiz.locator('p').inner_text(); quiz.get_by_role('button',name='审核').click(); assert '再想想' in quiz.locator('p').inner_text()
 steps=page.locator('article[data-type=steps]'); steps.get_by_role('button').click(); assert steps.locator('rect').nth(1).get_attribute('opacity')=='1'
 page.goto('about:blank'); load(page,'templates/lesson.html','../assets/visuals.js'); assert page.locator('#title').inner_text().startswith('S01'); page.locator('#next').click(); assert page.locator('#title').inner_text().startswith('S02'); page.locator('nav button').nth(2).click(); assert page.locator('#title').inner_text().startswith('S03'); page.locator('#next').click(); assert '未知信息' in page.locator('#note').inner_text(); page.locator('#title').click(); page.keyboard.press('ArrowRight'); assert page.locator('#title').inner_text().startswith('S04'); page.keyboard.press('ArrowLeft'); assert page.locator('#title').inner_text().startswith('S03'); page.locator('nav button').last.click(); assert page.locator('#next').is_disabled(); page.locator('nav button').first.click(); assert page.locator('#prev').is_disabled()
 page.locator('#full').click(); page.wait_for_timeout(200); fullscreen=page.evaluate('!!document.fullscreenElement'); print('fullscreen:',fullscreen); 
 if fullscreen: page.locator('#full').click(); page.wait_for_timeout(100)
 page.locator('nav button').nth(3).click(); print('26 SVG, quiz, steps, nav, step progression, keyboard, boundaries; page errors:',errors); assert not errors
 b.close()
