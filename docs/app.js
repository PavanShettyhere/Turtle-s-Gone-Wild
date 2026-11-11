'use strict';
const boxes=[...document.querySelectorAll('[data-key]')];
const storageKey='turtle-journal-reading-v1';
let saved={};
try { saved=JSON.parse(localStorage.getItem(storageKey)||'{}')||{}; } catch {}
function progress(){const n=boxes.filter(b=>b.checked).length;document.querySelector('#progress').value=100*n/boxes.length;document.querySelector('#progress-label').textContent=`${n} / ${boxes.length} steps reviewed`;}
boxes.forEach(b=>{b.checked=saved[b.dataset.key]===true;b.addEventListener('change',()=>{saved[b.dataset.key]=b.checked;try{localStorage.setItem(storageKey,JSON.stringify(saved));}catch{}progress();});});
progress();
document.querySelector('#reset').addEventListener('click',()=>{saved={};boxes.forEach(b=>b.checked=false);try{localStorage.removeItem(storageKey);}catch{}progress();});
let timer;function toast(message){const el=document.querySelector('#toast');el.textContent=message;clearTimeout(timer);timer=setTimeout(()=>el.textContent='',3500);}
document.querySelectorAll('.copy').forEach(button=>button.addEventListener('click',async()=>{const code=button.closest('.command').querySelector('code');try{await navigator.clipboard.writeText(code.textContent);toast('Command copied. Check the target machine before running.');}catch{const range=document.createRange();range.selectNodeContents(code);const selection=window.getSelection();selection.removeAllRanges();selection.addRange(range);toast('Copy unavailable. Command selected; use Ctrl+C or ⌘C.');}}));
const details=[...document.querySelectorAll('details')];
const search=document.querySelector('#search');
search.addEventListener('input',()=>{const q=search.value.toLowerCase().trim();let found=0;document.querySelectorAll('.chapter').forEach(ch=>{const steps=[...ch.querySelectorAll('.step')];if(!steps.length)return;let hits=0;steps.forEach(s=>{const match=!q||s.textContent.toLowerCase().includes(q);s.hidden=!match;if(match){hits++;if(q)s.open=true;}});ch.hidden=hits===0;found+=hits;});document.querySelector('#search-status').textContent=q?`${found} matching steps`:'';});
document.querySelector('#expand-all').addEventListener('click',event=>{const open=event.target.textContent==='Expand all';details.forEach(d=>d.open=open);event.target.textContent=open?'Collapse all':'Expand all';});
let beforePrint;
window.addEventListener('beforeprint',()=>{beforePrint=[...document.querySelectorAll('.chapter,.step')].map(el=>({el,hidden:el.hidden,open:el.open}));beforePrint.forEach(({el})=>{el.hidden=false;if(el.tagName==='DETAILS')el.open=true;});});
window.addEventListener('afterprint',()=>{(beforePrint||[]).forEach(({el,hidden,open})=>{el.hidden=hidden;if(el.tagName==='DETAILS')el.open=open;});});
document.querySelector('#print').addEventListener('click',()=>window.print());
