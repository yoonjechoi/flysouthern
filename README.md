# flysouthern


## Development setup
1. Install pyenv : https://github.com/pyenv/pyenv#basic-github-checkout
2. Install pyenv plugin for virtualenv https://github.com/pyenv/pyenv-virtualenv
3. Run
    ```
    $ pyenv install 3.4.3 && pyenv virtualenv 3.4.3 flysouthern-server
    ```
4. Run 
    ```
    $ mkdir ~/git-repo && cd git-repo && git clone https://github.com/yoonjechoi/flysouthern && cd fintorrent-server
    ```
    터미널창의 프롬프트가 (fintorrent-server)라는 prefix가 붙어있는 것을 확인
    ```
    (flysouthern-server) Choiui-MacBook-Pro:flysouthern-server yoonjechoi$
    ```
    ### 앞으로의 모든 터미널 명령문은  (fintorrent-server) 가 맨앞에 붙은 상태에서 실행되야한다.

5. pip install
    ```
    (fintorrent-server) $ pip install --upgrade pip && pip install -r ./requirements.txt
    ```
6. ~/git-repo/flysouthern-server/flysouthern django project root다.
    ```
    $ cd ~/git-repo/fintorrent-server/flysouthern
    (flysouthern-server)$ python manage.py test
    ```
 
