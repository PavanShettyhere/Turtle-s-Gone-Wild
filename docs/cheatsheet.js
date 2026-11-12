'use strict';
const cards=[...document.querySelectorAll('.cheat-card')];
const search=document.querySelector('#cheat-search');
const category=document.querySelector('#cheat-category');
function filter(){const q=search.value.trim().toLowerCase();let count=0;cards.forEach(card=>{const match=(!q||card.textContent.toLowerCase().includes(q))&&(category.value==='all'||card.dataset.category===category.value);card.hidden=!match;if(match)count++;});document.querySelector('#cheat-status').textContent=count?`${count} ${count===1?"command":"commands"} ready to use`:'No matches. Try another search or select All commands.';}
search.addEventListener('input',filter);category.addEventListener('change',filter);filter();
let timer;function toast(message){document.querySelector('#toast').textContent=message;clearTimeout(timer);timer=setTimeout(()=>document.querySelector('#toast').textContent='',3500);}
document.querySelectorAll('.copy').forEach(button=>button.addEventListener('click',async()=>{const code=button.closest('.command').querySelector('code');try{await navigator.clipboard.writeText(code.textContent);toast('Copied. Paste into the terminal shown on this card.');}catch{const range=document.createRange();range.selectNodeContents(code);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Command selected. Press Ctrl+C or ⌘C to copy.');}}));
