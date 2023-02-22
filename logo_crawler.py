import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# def check_cafe24(soup):
#     scripts = soup.find_all('script')
#     for script in scripts:
#         str_script=str(script)
#         if "cafe24" in str_script:
#           return True

def del_sfx(url):
  sfx=["www.","http://","https://",".com/",".co.kr/",".com",".co.kr",".kr/",".kr"]
  for s in sfx:
    url=url.replace(s,"")
  return url  
  
def save_logo(logo_element,url,count):
  shop=del_sfx(url)
  image_src = logo_element.find('img')['src']
  image_url = urljoin(url, image_src)
  print(image_url)
  response = requests.get(image_url,headers={"User-Agent": "Mozilla/5.0"})
  ext="."+image_src.split('.')[-1]
  filename=f'{shop}_{count}'+ext
  with open(filename, 'wb') as f:
    f.write(response.content)
    print(f'Logo image saved as {filename}')

def extract_logo_image(url):
    # Get the HTML content of the webpage
    response = requests.get(url,headers={"User-Agent": "Mozilla/5.0"})
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    logo_elements = soup.find_all(class_=lambda x: x and (('logo' in x) or ('Logo' in x)))
    if logo_elements:
      count=1
      for logo_element in logo_elements:
        if logo_element.find('img'):
          save_logo(logo_element,url,count)
          count+=1
      return True
                
    else:
      print('No logo element found')
      return False


if __name__=="__main__":
    url="www.xexymix.com" # url은 www, http://, https://로 시작해서 .co.kr, .com 으로 끝나야 함
    extract_logo_image(url)