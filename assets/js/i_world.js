let image = document.querySelectorAll('.content img'); //이미지 개수 =>2개
console.log("check");
let end = 1;
//console.log(image)

// 이미지 로딩
let image_list1 = [
    'images/interior/s0.jpg',
    'images/interior/s1.jpg',
    'images/interior/s2.jpg',
    'images/interior/s3.jpg',
    'images/interior/s4.jpg',
    'images/interior/s5.jpg',
    'images/interior/s6.jpg',
    'images/interior/s7.jpg',
    'images/interior/s8.jpg',
    'images/interior/s9.jpg',
    'images/interior/s10.jpg',
    'images/interior/s11.jpg',
    'images/interior/s12.jpg',
    'images/interior/s13.jpg',
    'images/interior/s14.jpg',
    'images/interior/s15.jpg',
    'images/interior/s16.jpg',
    'images/interior/s17.jpg',
    'images/interior/s18.jpg',
    'images/interior/s19.jpg',
    'images/interior/s20.jpg',
    'images/interior/s21.jpg',
    'images/interior/s22.jpg',
    'images/interior/s23.jpg',
    'images/interior/s24.jpg',
    'images/interior/s25.jpg',
    'images/interior/s26.jpg',
    'images/interior/s27.jpg',
    'images/interior/s28.jpg',
    'images/interior/s29.jpg',
    'images/interior/s30.jpg',
    'images/interior/s31.jpg'];

//셔플
function shuffle(a) {
    let j, x, i;
    for (i = a.length; i; i -= 1) {
        j = Math.floor(Math.random() * i);
        x = a[i - 1];
        a[i - 1] = a[j];
        a[j] = x;
    }
}

shuffle(image_list1);



let image_list2 = [];

let world = 16; //32강 -> 16 8 4 2 진행
let now_image = 0; //현재 이미지 순서
image[0].setAttribute('src', `${image_list1[now_image]}`);
image[1].setAttribute('src', `${image_list1[now_image + 1]}`);



// console.log(image_list1);
// console.log(image_list2);
//이미지 선택 이벤트
for (let i = 0; i < image.length; i++) {
    image[i].addEventListener('click', function () {
        if (end == 1) {
            let select_img = this.getAttribute('src');
            let title_text = document.querySelector('.text');
            const content = document.querySelector('.content')
            const title = document.querySelector('.title');
            

            click_img = this.getAttribute('class');//선택된 이미지 확인해보기

            //선택된 이미지 배열에 넣는 곳
            if (click_img == 'img2' && (world == 16 || world == 4)) {
                image_list2.push(select_img);
            }
            else if (click_img == 'img1' && (world == 16 || world == 4)) {
                image_list2.push(select_img);
            }
            else if (click_img == 'img2' && (world == 8 || world == 2)) {
                image_list1.push(select_img);
            }
            else if (click_img == 'img1' && (world == 8 || world == 2)) {
                image_list1.push(select_img);
            }
            else if (click_img == 'img2' && (world == 4 || world == 1)) {
                image_list2.push(select_img);
            }
            else if (click_img == 'img1' && (world == 4 || world == 1)) {
                image_list2.push(select_img);
            }

            //선택된 이미지 애니메이션 효과
            if (click_img == 'img2' && world != 0) {
                console.log('img2클릭')

            } else if (click_img == 'img1' && world != 0) {
                console.log('img1클릭')
            }

            //다음페이지 변수 바꾸기
            if (world == 16 && now_image == 30) {
                now_image = 0;
                world = 8;
                image_list1 = [];
            }
            else if (world == 8 && now_image == 14) {
                now_image = 0;
                world = 4;
                image_list2 = [];
            }
            else if (world == 4 && now_image == 6) {
                now_image = 0;
                world = 2;
                image_list1 = [];
            }
            else if (world == 2 & now_image == 2) {
                now_image = 0;
                world = 1;
                image_list2 = [];
            }
            else if (world == 1 & now_image == 0) {
                world = 0;
                image_list1 = [];
            }
            else {
                now_image += 2;
            }

            //문구 변경
            if (world == 16 || world == 4 || world == 1) {
                title_text.innerHTML = `<h1>인테리어 월드컵 32강 (${(now_image + 2) / 2}/${world})</h1>`;
                image[0].setAttribute('src', `${image_list1[now_image]}`);
                image[1].setAttribute('src', `${image_list1[now_image + 1]}`);
            } else if (world == 8 || world == 2) {
                title_text.innerHTML = `<h1>인테리어 월드컵 32강 (${(now_image + 2) / 2}/${world})</h1>`;
                image[0].setAttribute('src', `${image_list2[now_image]}`);
                image[1].setAttribute('src', `${image_list2[now_image + 1]}`);
            } else {

                //결과 보여주기
               /* title_text.innerHTML = `<h1>결과</h1>`;*/
                title.className = 'title fade-in';
            	
                image[0].setAttribute('src', `${image_list2[now_image]}`);
                let image_style = image_list2[now_image];
                let arr1 = image_style.split('/');
                let arr2 = arr1[3].split('_');
                image_style = arr2[0]; //이미지 파일 이름 꺼내오기
                
                const content = document.querySelector('.content')

                //photo2 div 제거
                const photo2 = document.querySelector('.photo2');
                content.removeChild(photo2);

                //result div 생성한 후 이어주기
                let result_div = document.createElement('div');
                result_div.className = 'result'; //생성된 div에 클래스이름 집어 넣기
                let result = document.createElement('h1');
                let result_text = document.createTextNode(image_style.toUpperCase()); //문구 대문자

                let product_btn =  document.createElement('button');
                let product_a = document.createElement('a');
                product_a.create
                product_a.appendChild(product_btn);
                product_a.appendChild
                product_btn.id = image_style; //생성된 버튼에 아이디 넣기
                product_btn.className = 'move';
                let btn_text = document.createTextNode('상품보러가기');

                result.appendChild(result_text);
                product_btn.appendChild(btn_text);
                result_div.appendChild(result);
                result_div.appendChild(product_btn);
                content.appendChild(result_div);
                
                
                btn = document.querySelector('.move');
                
                btn.addEventListener('click',function(){
                    location.href = `ResearchService.do?id=${image_style}`;
                });
                
                
                end=0; //이벤트 더 이상 적용하지 않게 하기
            }
        }
    })
}