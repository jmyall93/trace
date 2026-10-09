"""TRACE Edge v1.3 guided onboarding. Deliberately no live OT connection in this candidate."""
import json, os, pathlib, tkinter as tk
from tkinter import ttk, messagebox
from urllib.parse import urlparse
from datetime import datetime

ROOT=pathlib.Path(os.getenv('LOCALAPPDATA',str(pathlib.Path.home()))) / 'TRACE Edge'
ROOT.mkdir(parents=True,exist_ok=True)
FILE=ROOT/'settings.json'
DEFAULT={'cloud_url':'https://trace.jeffmyall6.workers.dev','servers':[],'approved':[],'poll_seconds':15,'setup_complete':False}
try:
    cfg=json.loads(FILE.read_text(encoding='utf-8')) if FILE.exists() else DEFAULT.copy()
    if not isinstance(cfg,dict):cfg=DEFAULT.copy()
except (ValueError,OSError):cfg=DEFAULT.copy()
for k,v in DEFAULT.items():cfg.setdefault(k,v)

BG='#0c131e';PANEL='#142234';PANEL2='#1b2c41';FG='#eaf2fc';MUTED='#99abc1';BLUE='#4b9bff';GREEN='#6ce4b2'
root=tk.Tk();root.title('TRACE Edge  |  Setup & Monitoring');root.geometry('1120x740');root.minsize(980,650);root.configure(bg=BG)
style=ttk.Style();style.theme_use('clam')
style.configure('TFrame',background=BG)
style.configure('TLabel',background=BG,foreground=FG,font=('Segoe UI',10))
style.configure('TEntry',padding=9,fieldbackground='#eaf1f8',foreground='#132033')
style.configure('TButton',font=('Segoe UI',10,'bold'),padding=(13,10))
style.configure('Treeview',background=PANEL,fieldbackground=PANEL,foreground=FG,rowheight=30,borderwidth=0,font=('Segoe UI',10))
style.configure('Treeview.Heading',background=PANEL2,foreground=FG,font=('Segoe UI',10,'bold'))
style.map('Treeview',background=[('selected','#225084')])

def label(parent,text,size=10,color=FG,bold=False,bg=None):
    return tk.Label(parent,text=text,font=('Segoe UI',size,'bold' if bold else 'normal'),bg=bg or BG,fg=color,anchor='w',justify='left')
def card(parent):return tk.Frame(parent,bg=PANEL,highlightbackground='#2c4059',highlightthickness=1)
def persist():
    FILE.write_text(json.dumps(cfg,indent=2),encoding='utf-8')
def clear(parent):
    for w in parent.winfo_children():w.destroy()
def action(parent,text,command,primary=False):
    return tk.Button(parent,text=text,command=command,bg=BLUE if primary else PANEL2,fg='#071422' if primary else FG,activebackground='#8fc0ff',activeforeground='#071422',font=('Segoe UI',10,'bold'),relief='flat',padx=18,pady=11,cursor='hand2',bd=0)
def field(parent,title,value='',secret=False):
    label(parent,title,10,MUTED,bg=PANEL).pack(anchor='w',pady=(14,5))
    e=tk.Entry(parent,font=('Segoe UI',11),show='*' if secret else '',bg='#eaf1f8',fg='#142034',relief='flat',insertbackground='#142034')
    e.insert(0,value);e.pack(fill='x',ipady=10)
    return e

shell=tk.Frame(root,bg=BG);shell.pack(fill='both',expand=True)
sidebar=tk.Frame(shell,bg='#0f1b2b',width=245);sidebar.pack(side='left',fill='y');sidebar.pack_propagate(False)
label(sidebar,'TRACE',25,FG,True,'#0f1b2b').pack(anchor='w',padx=25,pady=(30,0))
label(sidebar,'EDGE  /  v1.4',11,BLUE,True,'#0f1b2b').pack(anchor='w',padx=26,pady=(0,26))
nav=tk.Frame(sidebar,bg='#0f1b2b');nav.pack(fill='x')
label(sidebar,'READ-ONLY BY DESIGN',9,GREEN,True,'#0f1b2b').pack(side='bottom',anchor='w',padx=23,pady=26)
main=tk.Frame(shell,bg=BG);main.pack(side='left',fill='both',expand=True)
header=tk.Frame(main,bg=BG);header.pack(fill='x',padx=30,pady=(27,12))
content=tk.Frame(main,bg=BG);content.pack(fill='both',expand=True,padx=30,pady=(5,25))
page='Overview'
buttons={}

def heading(title,subtitle):
    clear(header)
    label(header,title,24,FG,True).pack(anchor='w')
    label(header,subtitle,10,MUTED).pack(anchor='w',pady=(6,0))
def note(parent,title,body):
    box=card(parent);box.pack(fill='x',pady=9)
    label(box,title,12,FG,True,PANEL).pack(anchor='w',padx=18,pady=(15,4))
    label(box,body,10,MUTED,bg=PANEL).pack(anchor='w',padx=18,pady=(0,16))

def render_overview():
    heading('Welcome to TRACE Edge','Your guided connection setup. No industrial networking knowledge required for routine use.')
    note(content,'Your setup at a glance','1  Connect TRACE Cloud       2  Add your server       3  Review tags       4  Start monitoring')
    tiles=tk.Frame(content,bg=BG);tiles.pack(fill='x',pady=12)
    for title,value,detail in [('TRACE Cloud','Not enrolled','Cloud enrollment must be verified'),('OPC UA Servers',str(len(cfg['servers'])),'Configured locally'),('Approved Tags',str(len(cfg['approved'])),'Awaiting secure discovery'),('Collector','Not running','Production collection disabled')]:
        c=card(tiles);c.pack(side='left',fill='both',expand=True,padx=(0,10))
        label(c,title,10,MUTED,bg=PANEL).pack(anchor='w',padx=14,pady=(15,6))
        label(c,value,15,FG,True,PANEL).pack(anchor='w',padx=14)
        label(c,detail,9,MUTED,bg=PANEL).pack(anchor='w',padx=14,pady=(6,17))
    note(content,'Security status  •  Pilot mode','No PLC writes, no remote-control tunnel and no production OPC UA sessions.\nSecure certificate enrollment and service operation are still being implemented.')
    action(content,'Begin guided setup  →',lambda:show('Connect Cloud'),True).pack(anchor='w',pady=18)

def render_cloud():
    heading('Connect TRACE Cloud','Link this gateway to your company’s TRACE account.')
    c=card(content);c.pack(fill='x',pady=15)
    inner=tk.Frame(c,bg=PANEL);inner.pack(fill='x',padx=22,pady=18)
    url=field(inner,'TRACE Cloud address',cfg['cloud_url'])
    label(inner,'Your organization will generate a one-time enrollment code in TRACE Cloud.',10,MUTED,bg=PANEL).pack(anchor='w',pady=(16,5))
    label(inner,'Enrollment is not active in this release. Never enter a production token here.',10,'#f6c979',bg=PANEL).pack(anchor='w')
    def save():
        u=url.get().strip();p=urlparse(u)
        if p.scheme!='https' or not p.netloc or p.username or p.password:messagebox.showerror('Check address','Enter a valid HTTPS TRACE Cloud URL.');return
        cfg['cloud_url']=u.rstrip('/');persist();messagebox.showinfo('Saved','Cloud address saved locally.\nDevice enrollment has not been completed.')
    action(inner,'Save cloud address',save,True).pack(anchor='w',pady=18)
    note(content,'What happens next?','A future secure enrollment step will pair this device using a short-lived code and device identity.\nThis release does not claim to have paired your computer.')

def render_servers():
    heading('OPC UA Connections','Add a FactoryTalk or Honeywell server without editing configuration files.')
    row=tk.Frame(content,bg=BG);row.pack(fill='x',pady=(10,16))
    action(row,'+ Add OPC UA server',add_server,True).pack(side='left')
    action(row,'Remove selected',remove_server).pack(side='left',padx=10)
    global server_tree
    server_tree=ttk.Treeview(content,columns=('type','endpoint','state'),show='headings',height=9)
    for key,title,width in [('type','System',155),('endpoint','OPC UA endpoint',360),('state','Status',150)]:server_tree.heading(key,text=title);server_tree.column(key,width=width,stretch=True)
    server_tree.pack(fill='both',expand=True)
    for i,s in enumerate(cfg['servers']):server_tree.insert('', 'end',iid=str(i),values=(s['type'],s['endpoint'],'Not connected'))
    note(content,'Connection testing','Production endpoint tests are intentionally disabled until certificate trust and server-enforced read-only access are implemented.')

def add_server():
    win=tk.Toplevel(root);win.title('Add an OPC UA server');win.geometry('560x500');win.configure(bg=BG);win.transient(root);win.grab_set()
    body=tk.Frame(win,bg=PANEL);body.pack(fill='both',expand=True,padx=18,pady=18)
    label(body,'Add an OPC UA server',19,FG,True,PANEL).pack(anchor='w',padx=15,pady=(15,0))
    label(body,'Ask your controls/IT team for the OPC UA endpoint address.',10,MUTED,bg=PANEL).pack(anchor='w',padx=15,pady=(4,0))
    form=tk.Frame(body,bg=PANEL);form.pack(fill='x',padx=15)
    name=field(form,'Connection name','Main Plant PLC')
    label(form,'Equipment platform',10,MUTED,bg=PANEL).pack(anchor='w',pady=(14,5))
    kind=ttk.Combobox(form,values=['Rockwell / FactoryTalk','Honeywell / Niagara','Other OPC UA'],state='readonly');kind.current(0);kind.pack(fill='x')
    endpoint=field(form,'OPC UA endpoint (example: opc.tcp://server:4840)','')
    label(form,'Read-only access must be enforced on the OPC UA server.',10,GREEN,bg=PANEL).pack(anchor='w',pady=(15,4))
    def save():
        n=name.get().strip();e=endpoint.get().strip();p=urlparse(e)
        if not n or p.scheme!='opc.tcp' or not p.hostname or not p.port:messagebox.showerror('Check details','Enter a name and a valid opc.tcp://host:port endpoint.',parent=win);return
        if any(s['name'].lower()==n.lower() for s in cfg['servers']):messagebox.showerror('Duplicate','Choose a different connection name.',parent=win);return
        cfg['servers'].append({'name':n,'type':kind.get(),'endpoint':e,'status':'not_connected'});persist();win.destroy();show('Connections')
    action(form,'Save server',save,True).pack(anchor='w',pady=20)

def remove_server():
    sel=server_tree.selection()
    if not sel:return
    i=int(sel[0]);name=cfg['servers'][i]['name']
    if messagebox.askyesno('Remove connection',f'Remove {name}? This does not change your PLC or BMS.'):
        cfg['servers'].pop(i);cfg['approved']=[p for p in cfg['approved'] if p.get('server')!=name];persist();show('Connections')

def render_tags():
    heading('Tag Discovery','Choose exactly what TRACE is allowed to observe.')
    note(content,'How discovery will work','Connect to a verified OPC UA server, browse its address space, select the points you need,\nthen approve the monitoring list. Nothing is automatically enabled.')
    label(content,'Approved monitoring list',13,FG,True).pack(anchor='w',pady=(20,10))
    tree=ttk.Treeview(content,columns=('server','name','node'),show='headings',height=8)
    for k,t in [('server','Server'),('name','Tag'),('node','Node ID')]:tree.heading(k,text=t);tree.column(k,width=230)
    tree.pack(fill='both',expand=True)
    for p in cfg['approved']:tree.insert('','end',values=(p.get('server',''),p.get('label',''),p.get('id','')))
    note(content,'Discovery not enabled yet','Secure OPC UA certificate trust and role permissions must be implemented before live browsing.\nThis screen does not generate fake tags or claim to discover connected equipment.')

def render_security():
    heading('Security Center','TRACE Edge is an observation-only gateway.')
    for title,body in [('READ ONLY  •  Permanent product policy','No Write, Call, alarm acknowledgement, setpoint changes or PLC programming.'),('Network boundary','No inbound connections from TRACE Cloud to the customer’s industrial network.'),('OPC UA certificates  •  Pending','Trusted certificate management, Sign & Encrypt, and server-side read-only roles are required.'),('Secrets and identity  •  Pending','Device enrollment and OS-protected credentials must be completed before production use.'),('Customer approval','Each site owner must approve endpoint access, polling load and tag allowlists.')]:note(content,title,body)

def render_diagnostics():
    heading('Diagnostics','Understand what is connected and what needs attention.')
    note(content,'Application','TRACE Edge v1.3 — guided setup preview\nLocal configuration: '+str(FILE))
    note(content,'Cloud status','Not enrolled — device identity and live health checks are not yet available.')
    note(content,'Industrial connections',f'{len(cfg["servers"])} saved servers · 0 active sessions · 0 active subscriptions')
    note(content,'Collection service','Not installed as a Windows Service. No background polling is running.')
    action(content,'Open configuration folder',lambda:os.startfile(str(ROOT)) if os.name=='nt' else None).pack(anchor='w',pady=15)

def render_settings():
    heading('Settings','Simple site preferences. Industrial configuration stays local.')
    c=card(content);c.pack(fill='x',pady=15)
    inner=tk.Frame(c,bg=PANEL);inner.pack(fill='x',padx=20,pady=15)
    interval=field(inner,'Requested polling interval (seconds)',str(cfg['poll_seconds']))
    def save():
        try:v=int(interval.get());assert 5<=v<=3600
        except (ValueError,AssertionError):messagebox.showerror('Check interval','Use a number between 5 and 3600 seconds.');return
        cfg['poll_seconds']=v;persist();messagebox.showinfo('Saved','Preference saved. Collection remains disabled.')
    action(inner,'Save preferences',save,True).pack(anchor='w',pady=18)
    note(content,'Need assistance?','Your site controls or IT administrator can supply the OPC UA endpoint and read-only account.\nTRACE Edge will guide the rest after secure onboarding is completed.')

PAGES={'Overview':render_overview,'Connect Cloud':render_cloud,'Connections':render_servers,'Tag Discovery':render_tags,'Security':render_security,'Diagnostics':render_diagnostics,'Settings':render_settings}
def show(which):
    global page
    page=which;clear(content)
    for name,button in buttons.items():button.configure(bg='#20446b' if name==which else '#0f1b2b',fg=FG if name==which else MUTED)
    PAGES[which]()
for name in PAGES:
    b=tk.Button(nav,text=('  '+name),anchor='w',font=('Segoe UI',11),bg='#0f1b2b',fg=MUTED,relief='flat',bd=0,padx=24,pady=15,activebackground='#20446b',activeforeground=FG,cursor='hand2',command=lambda n=name:show(n))
    b.pack(fill='x');buttons[name]=b
show('Overview')
root.mainloop()
