const API_BASE = '/api/v1';
const sessionId = 'web-session-1';
const userId = 'web-user-1';

const messagesEl = document.getElementById('messages');
const formEl = document.getElementById('chat-form');
const inputEl = document.getElementById('message');
const clarificationEl = document.getElementById('clarification');
const clarificationQuestionEl = document.getElementById('clarification-question');
const clarificationOptionsEl = document.getElementById('clarification-options');
const memoryListEl = document.getElementById('memory-list');
const taskPanelEl = document.getElementById('task-panel');
const taskIdEl = document.getElementById('task-id');
const taskStepsEl = document.getElementById('task-steps');
const taskTimelineEl = document.getElementById('task-timeline');
const retryBtn = document.getElementById('retry-task');
let lastAgentMessage = '';

function appendMessage(role, text) { const div = document.createElement('div'); div.className='msg'; div.innerHTML=`<span class="role">${role}:</span> ${text}`; messagesEl.appendChild(div); messagesEl.scrollTop=messagesEl.scrollHeight; }
function renderTask(data) {
  if (!data.task_id) { taskPanelEl.classList.add('hidden'); return; }
  taskPanelEl.classList.remove('hidden');
  taskIdEl.textContent = `task_id: ${data.task_id}`;
  taskStepsEl.innerHTML = '';
  (data.steps || []).forEach((s) => { const li = document.createElement('li'); li.textContent = `${s.name} [${s.status}]`; taskStepsEl.appendChild(li); });
  taskTimelineEl.innerHTML = '';
  (data.timeline || []).forEach((t) => { const li = document.createElement('li'); li.textContent = `${t.tool} - ${t.status}: ${t.message}`; taskTimelineEl.appendChild(li); });
  retryBtn.disabled = !data.can_retry;
}

async function fetchMemory(){const res=await fetch(`${API_BASE}/memory/${sessionId}`);const items=await res.json();memoryListEl.innerHTML='';items.forEach((item)=>{const li=document.createElement('li');li.innerHTML=`<div><b>${item.role}</b>: ${item.content}</div><div class="small">id: ${item.id}</div><button data-id="${item.id}" data-action="edit">编辑</button><button data-id="${item.id}" data-action="delete">删除</button>`;memoryListEl.appendChild(li);});}

async function sendChat(message, forcedType='auto'){appendMessage('user',message);const res=await fetch(`${API_BASE}/chat`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:userId,session_id:sessionId,message,request_type:forcedType})});const data=await res.json();appendMessage('assistant',data.answer);if(data.plan&&data.plan.length){appendMessage('plan',data.plan.join(' -> '));} renderTask(data); if(data.route==='agent'){ lastAgentMessage = message; }
if(data.needs_clarification){clarificationEl.classList.remove('hidden');clarificationQuestionEl.textContent=data.clarification_question||'请补充信息';clarificationOptionsEl.innerHTML='';data.clarification_options.forEach((opt)=>{const btn=document.createElement('button');btn.textContent=opt.label;btn.onclick=()=>{if(opt.value==='custom'){inputEl.focus();inputEl.placeholder='请补充具体目标、约束、期望输出';return;}sendChat(`我选择：${opt.label}`,opt.value);clarificationEl.classList.add('hidden');};clarificationOptionsEl.appendChild(btn);});}else{clarificationEl.classList.add('hidden');}fetchMemory();}

formEl.addEventListener('submit',async(e)=>{e.preventDefault();const msg=inputEl.value.trim();if(!msg)return;inputEl.value='';await sendChat(msg);});
retryBtn.addEventListener('click', async () => { if (!lastAgentMessage) return; await sendChat(`重试任务：${lastAgentMessage}`, 'agent'); });
document.getElementById('refresh-memory').addEventListener('click',fetchMemory);
memoryListEl.addEventListener('click',async(e)=>{const target=e.target;if(!(target instanceof HTMLButtonElement))return;const id=target.dataset.id;const action=target.dataset.action;if(!id||!action)return;if(action==='delete'){await fetch(`${API_BASE}/memory/${sessionId}/${id}`,{method:'DELETE'});fetchMemory();}if(action==='edit'){const content=prompt('输入新记忆内容');if(!content)return;await fetch(`${API_BASE}/memory/${sessionId}/${id}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({content})});fetchMemory();}});
fetchMemory();
