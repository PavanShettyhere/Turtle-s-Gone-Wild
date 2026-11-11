"""Generate both journal formats from the same editable JSON source."""
import html,json,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
data=json.loads((root/'docs/journal.json').read_text())
e=html.escape
md=['# Turtle’s Gone Wild — Build journal','\nBy Pavan Shetty · Living notebook\n','> Evidence note: Day 1 milestones were reported by the author. Detailed commands are reference instructions, not recovered history. Day 2’s Pi setup is an explicit assumption awaiting confirmation. Expected output is never a claim of a completed test.\n']
sections=[]
for day in data['days']:
 md += ['## '+day['label']+' — '+day['title'],day['status'],day['intro']]
 steps=[]
 for i,s in enumerate(day['steps'],1):
  md += ['### '+str(i)+'. '+s['title'],'**Run on:** '+s['device'],s['body']]
  commands=[]
  for c in s['commands']:
   md += ['```bash\n'+c['code']+'\n```',c['why']]
   commands.append('<div class="command"><div class="command-top"><span>BASH</span><button class="copy" type="button">Copy command</button></div><pre><code>'+e(c['code'])+'</code></pre><p>'+e(c['why'])+'</p></div>')
  observed=''
  if s.get('output'):
   md += ['**Observed output (relevant lines supplied by the author):**', '```text\n'+s['output']+'\n```']
   observed='<div class="command"><div class="command-top">OBSERVED OUTPUT · AUTHOR-SUPPLIED EXCERPT</div><pre><code>'+e(s['output'])+'</code></pre></div>'
  md += ['**Checkpoint:** '+s['check'],'']
  body=''.join('<p>'+e(part).replace('\n','<br>')+'</p>' for part in s['body'].split('\n\n'))
  steps.append(f'<details class="step" id="{day["id"]}-step-{i}" open><summary><span class="step-no">{i:02}</span><span>{e(s["title"])}<small>{e(s["device"])}</small></span><span class="expand">+</span></summary><div class="step-body">{body}{"".join(commands)}{observed}<div class="checkpoint"><strong>CHECKPOINT</strong><p>{e(s["check"])}</p></div><label class="done"><input type="checkbox" data-key="{day["id"]}-{i}"> I’ve reviewed this step</label></div></details>')
 sections.append(f'<section class="chapter" id="{day["id"]}" aria-labelledby="{day["id"]}-title"><div class="eyebrow">{e(day["label"])} / FIELD NOTES</div><h2 id="{day["id"]}-title">{e(day["title"])}</h2><p class="chapter-sub">{e(day["subtitle"])}</p><div class="notice"><strong>{e(day["status"])}</strong><p>{e(day["intro"])}</p></div>{"".join(steps)}</section>')
md+=['## Troubleshooting','- `ros2: command not found`: source the Jazzy setup file in this terminal and verify installation.','- Package not found: check Ubuntu version, successful ROS apt-source installation, network access, and apt update errors.','- SSH refused: confirm the Pi has booted, its address is correct, and SSH is enabled.','- Listener receives nothing: test on one machine first; then check domain, subnet discovery, network isolation, and firewall rules. Do not disable the firewall blindly.','- Git origin already exists: inspect `git remote -v` before changing any URL.','- Push rejected: fetch and inspect remote changes; do not force-push over someone else’s work.','\n## Future days','Copy DAY-TEMPLATE.md to collect new notes; then append a chapter in docs/journal.json and regenerate with python3 scripts/build.py. Capture date, machine, goal, exact commands, explanation, actual output, errors/fixes, evidence, and next steps.','\n## References']
md+=['- ['+name+']('+url+')' for name,url in data['references']]
(root/'JOURNAL.md').write_text('\n\n'.join(md)+'\n')
links=''.join('<li><a href="'+e(url)+'">'+e(name)+' ↗</a></li>' for name,url in data['references'])
nav=''.join('<a href="#'+e(day['id'])+'">'+e(day['label'])+' <span>'+e(day['title'])+'</span></a>' for day in data['days'])
template=(root/'scripts/template.html').read_text().replace('<!-- DAY NAV -->',nav)
(root/'docs/index.html').write_text(template.replace('<!-- CHAPTERS -->',''.join(sections)).replace('<!-- REFERENCES -->',links))
(root/'docs/JOURNAL.md').write_text((root/'JOURNAL.md').read_text())
print('Built JOURNAL.md and docs/index.html from',len(data['days']),'chapters.')
