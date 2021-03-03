let image = document.querySelectorAll('.content img'); //이미지 개수 =>2개
console.log("check");
let end = 1;
//console.log(image)

// 이미지 로딩
let image_list1 = [
    '/static/images/worldcup/vs1_1.jpg',
    '/static/images/worldcup/vs2_1.jpg',
    '/static/images/worldcup/vs1_2.jpg',
    '/static/images/worldcup/vs2_2.jpg',
    '/static/images/worldcup/vs3_1.jpg',
    '/static/images/worldcup/vs3_2.jpg',
    '/static/images/worldcup/vs4_1.jpg',
    '/static/images/worldcup/vs4_2.jpg',
    '/static/images/worldcup/vs5_1.jpg',
    '/static/images/worldcup/vs5_2.jpg'
    ];

function plus_array(arr1, arr2) {
    var answer = Array();

    for (var i = 0; i < arr1.length; i++) {
        answer[i] = [];
        answer[i] = arr1[i] + arr2[i];
    }
    return answer;
}

// 스타일 확인하기
function style_check(image_list2) {
    if (Math.max.apply(null,image_list2) == image_list2[0]) {
        f_style = "러블리"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_lovely"
    }
    else if (Math.max.apply(null,image_list2) == image_list2[1]) {
        f_style = "캐주얼"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_casual"
    }
    else if (Math.max.apply(null,image_list2) == image_list2[2]) {
        f_style = "베이직"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_basic"
    }
    else if (Math.max.apply(null,image_list2) == image_list2[3]) {
        f_style = "모던시크"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_modernchic"
    }
    else if (Math.max.apply(null,image_list2) == image_list2[4]) {
        f_style = "유니크"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_unique"
    }
    else if (Math.max.apply(null,image_list2) == image_list2[5]) {
        f_style = "섹시"
        document.write('val :' + image_list2 + '<br>');
        location.href="/style_sexy"
    }
}


let image_list2 = [0,0,0,0,0,0];
let count_image_num = 0;
let world = 4; 
let now_image = 0; //현재 이미지 순서
image[0].setAttribute('src', `${image_list1[now_image]}`);
image[1].setAttribute('src', `${image_list1[now_image + 1]}`);

let f_style =""

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
            if (click_img == 'img1' && count_image_num == 0) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [100,0,0,0,0,0]);
            }
            else if (click_img == 'img2' && count_image_num == 0) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,0,0,10,0,90]);
            }
            else if (click_img == 'img1' && count_image_num == 1) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,0,0,0,0,100]);
            }
            else if (click_img == 'img2' && count_image_num == 1) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,0,0,30,70,0]);
            }
            else if (click_img == 'img1' && count_image_num == 2) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,20,0,80,0,0]);
            }
            else if (click_img == 'img2' && count_image_num == 2) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,0,0,90,0,10]);
            }
            else if (click_img == 'img1' && count_image_num == 3) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,0,0,0,100,0]);
            }
            else if (click_img == 'img2' && count_image_num == 3) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [20,80,0,0,0,0]);
            }
            else if (click_img == 'img1' && count_image_num == 4) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [0,100,0,0,0,0])
                style_check(image_list2)
            }
            else if (click_img == 'img2' && count_image_num == 4) {
                count_image_num = count_image_num + 1
                image_list2 = plus_array(image_list2, [80,0,20,0,0,0])
                style_check(image_list2)
            }

            

            //선택된 이미지 애니메이션 효과
            if (click_img == 'img2' && world != 0) {
                console.log('img2클릭')
                
            } else if (click_img == 'img1' && world != 0) {
                console.log('img1클릭')
            }

            //다음페이지 변수 바꾸기
            if (world == 4 && now_image == 10) {
                now_image = 6;
                world = 3;
                image_list1 = [];
            }
            else if (world == 3 & now_image == 6) {
                now_image = 4;
                world = 2;
                image_list2 = [];
            }
            else if (world == 2 & now_image == 4) {
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
                //title_text.innerHTML = `<h1>인테리어 월드컵 32강 (${(now_image + 2) / 2}/${world})</h1>`;
                image[0].setAttribute('src', `${image_list1[now_image]}`);
                image[1].setAttribute('src', `${image_list1[now_image + 1]}`);
            } else if (world == 8 || world == 2) {
                //title_text.innerHTML = `<h1>인테리어 월드컵 32강 (${(now_image + 2) / 2}/${world})</h1>`;
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
