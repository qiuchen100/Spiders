    text.send_keys('python')
    browser.find_element_by_id('su').submit()
    results = browser.find_elements_by_class_name('t')
    for result in results:
        print('标题：{}超链接：{}'.format(result.text, result.find_element_by_tag_name('a').get_attribute('href')))