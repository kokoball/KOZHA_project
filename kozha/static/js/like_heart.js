/*
	Snapshot by TEMPLATED
	templated.co @templatedco
	Released for free under the Creative Commons Attribution 3.0 license (templated.co/license)
*/

// heart
const buttons = document.querySelectorAll('.like-heart-btn')
for (const button of buttons) {
	button.addEventListener('click', function(){
		this.classList.toggle('active');
	  })
}
    