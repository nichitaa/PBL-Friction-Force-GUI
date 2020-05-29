import pdb
from tkinter import *
import tkinter.messagebox
import matplotlib.pyplot as plt

from tkinter import ttk
from collections import defaultdict
from tkinter.filedialog import *
from tkinter.messagebox import *
from tkinter import filedialog
import gspread


FrictionF_list = [] # pentru fortele de frecare
coefs = [] # pentru coeficientii de frecare
last = []

def find_error(all, fric, tau0, J, r, m_disc):

    friction = sum(fric) / len(fric) # media fortelor de frecare

    mas =[]
    vel = []
    t = []
    for i in range(len(all)):
        mas.append(all[i][0]) # toate masele introduse
        vel.append(all[i][1]) # toate w introduse
        t.append(all[i][2]) # toate timpurile tau introduse

    # media fiecarii din valori
    m = sum(mas) / len(mas)
    w = sum(vel) / len(vel)
    tau = sum(t) / len(t)
    tau0 = tau0

    # delata fiecarui din valori
    d_m = 0.005
    d_r = 0.005
    d_tau = 0.5
    d_tau0 = 0.5
    d_vel = 0.5

    # epsilon F
    eps_f = (  2*((d_m / m_disc) + (2*d_r / r)) + (2*d_vel/w) + (2*d_tau0/tau0) + (2*d_tau/tau) + (d_r/r) )
    # delata F
    d_f = friction * eps_f

    print('masa_average = ', m)
    print('w_average = ', w)
    print('tau_average = ', tau)
    print('tau0 = ', tau0)
    print('raza = ', r)
    print('masa_d = ', m_disc)
    print('Fric av = ', friction)
    print('Eps F = ', eps_f)
    print('Delt F = ', d_f)

    # actualizam datele in interfata
    delta_ff['text'] = '| ΔFᶠ = {:.3f}'.format(d_f)
    eps['text'] = '| \U0001D700 = {:.3f}%'.format(eps_f)

# pentru ultimul input + afisarea graficului dependentei
def Plot_the_graph(event):
    global tab, last, raza_discului, FrictionF_list, normalF_list, coefs, last, submit, raza, mas_disc, plot_btn
    # salvam datele introduse
    try:
        w__0 = float(viteza0.get())
        t__0 = float(tau0.get())
    except ValueError:
        ValueErrorPopUp()

    last.append([0, w__0, t__0])
    print('-------------------\n')
    # print(last)
    # includem datele in tabel
    tab[15, 2]['text'] = '\u03C90 ='.translate(SUB) + str(w__0)
    tab[15, 3]['text'] = '\u03C40 ='.translate(SUB) + str(t__0)
    tab[15, 4]['text'] = '\U0001D441 = 0' # F(N)
    M_for_0 = Momentul_fortei_disc(t__0, Momentum_J(mas_disc, raza_discului), w__0)
    tab[15, 5]['text'] = '\U0001D440 = {:.3f}'.format(M_for_0) # Momentul

    # dezactivam butoanele si stergem campurile
    viteza0.delete(0, END)
    tau0.delete(0, END)
    masa['state'] = DISABLED
    viteza['state'] = DISABLED
    tau['state'] = DISABLED
    tau0['state'] = DISABLED
    viteza0['state'] = DISABLED

    # calculam forta de frecare
    J = Momentum_J(mas_disc, raza_discului)
    for i in range(9):
        tau_current = general[i][2]
        print('tau curnt', tau_current)
        Friction = Friction_force(J, w__0, raza_discului,t__0, tau_current)
        FrictionF_list.append(Friction)

    # adugam forta de frecare in tabel
    j = 0
    for i in range(6, 15):
        tab[i, 5]['text'] = '{:.4f}'.format(FrictionF_list[j])
        j += 1

    # calculam coeful de frecare
    for i in range(9):
        k = Coeficient(FrictionF_list[i], normalF_list[i])
        coefs.append(k)
    # adaugam coeful de frecare in tabel
    j = 0
    for i in range(6, 15):
        tab[i, 6]['text'] = '{:.4f}'.format(coefs[j])
        j += 1
    tab[15, 6]['text'] = '\U0001D458 = 0' # pentru m = 0 , ---> k = 0

    # calculam si afisam erorile
    find_error(general, FrictionF_list, t__0, J, raza_discului, mas_disc)

    # functie pentru a afisa plotul
    def show_plot(event):
        # pdb.set_trace()
        global normalF_list, FrictionF_list
        plt.plot(normalF_list, FrictionF_list, 'b')
        plt.plot(normalF_list, FrictionF_list, 'ro')
        plt.grid()
        plt.ylabel('Forta de frecare Fᶠ (N)')
        plt.xlabel('Forta N (N)')
        plt.title('Graficul dependentei Fᶠ = f(N)')
        plt.show()

    # pdb.set_trace()
    plot_btn = Button(frame2, text="Plot the graph 📈", font="Times 11", width=20, bg=submit_color_btn, fg=txt_color,
                      activebackground=on_click)
    plot_btn.grid(row=4, column=4, padx=(5, 0), pady=(2, 5))
    plot_btn.bind("<Button-1>", show_plot) # afisam plotul la apasarea butonului


def Momentum_J(weight, raza_1):
    return (weight * (raza_1 ** 2)) / 2


def Momentul_fortei_disc(tau0, J, w0):
    return (J*w0)/tau0

# pentru restartarea experimentului, aducem toate widgeturile la starea initiala, si stergem toata datele salvate anterior
def Restart_experiment(event):
    # global taus , velocity, mass,step , ra, raza, add,
    # pdb.set_trace()
    global ra, raza, add, clearf, tab, step, restart, general, normalF_list, coefs, FrictionF_list, last, mass, masa_discului, plot_btn
    coefs.clear()
    general.clear()
    normalF_list.clear()
    FrictionF_list.clear()
    last.clear()
    plot_btn.grid_forget()
    submit.grid_forget()

    step = 5
    ra['text'] = 'Raza discului (m): '
    mass['text'] = 'Masa discului (kg) '
    masa_discului.delete(0, END)
    masa_discului.grid(row=3, column=4, pady=1, padx=2)
    mass.grid(row=1, column=4, pady=1, padx=2)
    mass.config(width=16)

    ra.grid(row=1, column=3, pady=1, padx=2)
    ra.config(width=15)
    raza.grid(row=3, column=3, pady=1, padx=2)

    clearf.grid_forget()
    add.grid_configure(row=4, column=3, padx=(5, 0))
    #
    restart.grid_configure(row=4, column=4, padx=(5, 0), pady=(1, 1))
    eps_r.grid_configure(row=2, column=3, padx=(5, 0))
    eps_m.grid_configure(row=2, column=4, padx=(5, 0))
    eps_common.grid_forget()

    add['state'] = NORMAL
    masa['state'] = NORMAL
    viteza['state'] = NORMAL
    tau['state'] = NORMAL

    # sterg datele tabelului
    for i in range(6, 16):
        for j in range(1, 7):
            tab[i, j]['text'] = ' '

    tab[15, 1]['text'] = 'masa = 0'
    tab[15, 2]['text'] = '\u03C90 =__'.translate(SUB)
    tab[15, 3]['text'] = '\u03C40 =__'.translate(SUB)
    tab[15, 4]['text'] = '\U0001D441 = 0' # N
    tab[15, 5]['text'] = '\U0001D440 =__'.translate(SUB) # M
    tab[15, 6]['text'] = '\U0001D458 = 0'

    delta_ff['text'] = '| ΔFᶠ = ___'
    eps['text'] = '| \U0001D700 = ___%'


def Friction_force(J, w0, R, tau_0, tau ):
    return ((J*w0) / (R*tau_0)) * ((tau_0/tau) - 1)


def Normal_force(m):
    return m * 9.8

# stergem campurile de entry
def clear_fields():
    masa.delete(0, END)
    viteza.delete(0, END)
    tau.delete(0, END)
    raza.delete(0, END)
    viteza0.delete(0, END)
    tau0.delete(0, END)
    masa_discului.delete(0, END)


def Coeficient(frecare, normala):
    return frecare / normala

# fereastra pop up ,  in caz ca valoarea introdusa nu e numar
def ValueErrorPopUp():
    clear_fields()
    popup = Tk()
    popup.bell()
    popup.geometry("400x100+500+140")
    popup.configure(bg=ufo)
    popup.resizable(0, 0)
    popup.wm_title('ValueError')
    label = Label(popup, text='Eroare Numerica: Introduceti un numar !', font="Times 15 italic")
    label.pack(side="top", fill="x", pady=10)
    B1 = Button(popup, text="Okay", font="Times 15 bold", command=popup.destroy)
    B1.pack()
    popup.mainloop()
    clear_fields()


def add_val(event):
    global taus, velocity, mass, step, ra, raza, add, general, normalF_list, raza_discului, raza_marime, masa_discului, mass, mas_disc
    # datele din entry
    try:
        m = float(masa.get())
        w = float(viteza.get())
        t = float(tau.get())
    # if not int
    except ValueError:
        ValueErrorPopUp() # pop up window

    # pentru prima introducere in tabel
    if step == 5:
        try:
            raza_discului = float(raza.get())
            mas_disc = float(masa_discului.get())

            ra['text'] = 'Raza = {:.2f}(m)'.format(raza_discului)
            ra.config(width=14)
            raza.grid_forget()
            mass['text'] = 'Masa discului = {:.2f}(kg)'.format(mas_disc)
            mass.config(width=20)
            masa_discului.grid_forget()
            eps_r.grid_forget()
            eps_m.grid_forget()
        except ValueError:
            ValueErrorPopUp()

    print('---------------\n')
    general.append([m, w, t])
    # print(general)

    # dupa primul input schimb pozitia butoanelor funcionale
    if step != 13:
        add.grid_configure(row = 2, column=3, padx=(5,0), pady=1)
        add.config(width=20)
        clearf.grid_configure(row = 3, column=3, padx=(5,0), pady=1)
        clearf.config(width=20)
        restart.grid_configure(row = 4, column=3, padx=(5,0), pady=1)
        restart.config(width=20)
        eps_common.grid(row = 2, column=4, padx=(5,0), pady=1)

    # stergem inputul precedent
    masa.delete(0, END)
    viteza.delete(0, END)
    tau.delete(0, END)
    raza.delete(0, END)

    # pentru penultimul input configuram butoanele si campurile de input
    if step == 13:
        clear_fields()
        add.grid_forget()
        add['state'], masa['state'], viteza['state'], tau['state'] = DISABLED, DISABLED, DISABLED, DISABLED
        tau0['state'], viteza0['state'], submit['state'] = NORMAL, NORMAL, NORMAL
        restart.grid_configure(row=2, column=3, padx=(5, 0), pady=(2, 5))
        submit.grid(row=4, column=3, padx=(5, 0), pady=(2, 5))

    # completam tabelul
    step += 1
    tab[step, 1]['text'] = '{:.2f}'.format(m)
    tab[step, 2]['text'] = '{:.2f}'.format(w)
    tab[step, 3]['text'] = '{:.2f}'.format(t)
    tab[step, 4]['text'] = '{:.3f}'.format(Normal_force(m))
    normalF_list.append(Normal_force(m))
    print('normal force list', normalF_list)


step = 5  # pentru a indexa in tabel datele, randul 0 in tabel e randul 5 in gridul general al paginii
general = [] # toate valorile introduse
normalF_list = [] # pentru forta normala
last = [] # pentru ultimile valori introduse , ( tau0, w0 )


def Import_data_Spreadsheets():
    global FrictionF_list, general, normalF_list, last, ra, raza, add, tab, coefs, r, t0, w0, mas_disc, mass, normalF_list, MM

    masa['state'], viteza['state'], tau['state'] = DISABLED, DISABLED, DISABLED
    viteza0['state'], tau0['state'] = DISABLED, DISABLED

    gc = gspread.service_account(filename='creds.json')
    sheet = gc.open_by_key('19FnHoinYGcMBgXQQi25YGXhC5ZSvAFwOs_WHKl_QdK8')
    worksheet = sheet.sheet1

    # lista de mase
    masa_list = worksheet.col_values(1)
    masa_list.pop(0)
    masa_list = [float(masa_list[i]) for i in range(len(masa_list))]

    # lista de viteze
    w = worksheet.col_values(2)
    w.pop(0)
    w = [float(w[i]) for i in range(len(w))]

    # lista de timput tau
    tau_list = worksheet.col_values(3)
    tau_list.pop(0)
    tau_list = [float(tau_list[i]) for i in range(len(tau_list))]

    # raza discului
    r = worksheet.get('D2')
    r = float(r[0][0])

    # masa discului
    mas_disc = worksheet.get('E2')
    mas_disc = float(mas_disc[0][0])

    # lisa cu toate valoarile
    general = []
    for i in range(9):
        general.append([masa_list[i], w[i], tau_list[i]])
    print('general - ', general)

    # viteza w0 si tau 0
    w0 = w[-1]
    t0 = tau_list[-1]
    tab[15, 2]['text'] = '\u03C90 = '.translate(SUB) + str(w0)
    tab[15, 3]['text'] = '\u03C40 = '.translate(SUB) + str(t0)
    tab[15, 4]['text'] = 0

    # Momentul de rezistenta
    MM = Momentul_fortei_disc(t0, Momentum_J(mas_disc, r), w0)
    tab[15, 5]['text'] = '\U0001D440 = {:.3f}'.format(MM)  # M

    ra['text'] = 'Raza = {:.2f}(m)'.format(r)
    mass['text'] = 'Masa discului = {:.2f}(kg)'.format(mas_disc)
    mass.config(width=20)
    masa_discului.grid_forget()
    eps_r.grid_forget()
    eps_m.grid_forget()

    ra.config(width=14)
    raza.grid_forget()
    print(FrictionF_list)

    # completez tabelul
    s = 6
    for i in range(0, 9):
        tab[s, 1]['text'] = '{:.2f}'.format(general[i][0])  # masa
        tab[s, 2]['text'] = '{:.2f}'.format(general[i][1])  # w0
        tab[s, 3]['text'] = '{:.2f}'.format(general[i][2])  # tau_0
        tab[s, 4]['text'] = '{:.3f}'.format(Normal_force(general[i][0]))  # F(N)
        s += 1
        normalF_list.append(Normal_force(general[i][0]))

    J = Momentum_J(mas_disc, r)
    print(J)
    print('tau_0', t0)
    for i in range(9):
        tau_current = general[i][2]
        print('tau curent', tau_current)
        Friction = Friction_force(J, w0, r, t0, tau_current)
        FrictionF_list.append(Friction)

    # forta de frecare coloana
    j = 0
    for i in range(6, 15):
        tab[i, 5]['text'] = '{:.4f}'.format(FrictionF_list[j])
        j += 1

    # completez tabelul cu coeful de frecare
    for i in range(9):
        k = Coeficient(FrictionF_list[i], normalF_list[i])
        coefs.append(k)
    j = 0
    for i in range(6, 15):
        tab[i, 6]['text'] = '{:.4f}'.format(coefs[j])
        j += 1
    tab[15, 6]['text'] = '\U0001D458 = 0'
    tab[15, 4]['text'] = '\U0001D441 = 0'  # N

    # aranjam butoanele
    add.grid_configure(row=2, column=3, padx=(5, 0), pady=1)
    add.config(width=20)
    clearf.grid_configure(row=3, column=3, padx=(5, 0), pady=1)
    clearf.config(width=20)
    restart.grid_configure(row=4, column=3, padx=(5, 0), pady=1)
    restart.config(width=20)
    eps_common.grid(row=2, column=4, padx=(5, 0), pady=1)

    # plot the data
    def Show_the_plot(normalF_list, FrictionF_list):
        plt.plot(normalF_list, FrictionF_list, 'b')
        plt.plot(normalF_list, FrictionF_list, 'ro')
        plt.grid()
        plt.xlabel('Forta N')
        plt.ylabel('Forta Fᶠ')
        plt.title('Graficul dependente Fᶠ = f(N)')
        plt.show()

    # Forces Lists / coefs
    print('friction - ',FrictionF_list )
    print('normal f - ',normalF_list )
    print('coefs - ', coefs)

    # afisam erorile
    find_error(general, FrictionF_list, t0, J, r, mas_disc)
    # afisam graficul
    Show_the_plot(normalF_list, FrictionF_list)


def Import_data():
    global FrictionF_list, general, normalF_list, last, ra, raza, add, tab, coefs, r, t0, w0, mas_disc, mass, normalF_list

    # disable all entrys:
    masa['state'], viteza['state'], tau['state'] = DISABLED, DISABLED, DISABLED
    viteza0['state'], tau0['state'] = DISABLED, DISABLED

    # deschid fisierul
    of = askopenfilename()
    file = open(of, "r")

    # citim valorile
    for i in range(0, 10):
        line = file.readline()
        listed = []
        for u in line.split(' '):
            listed.append(u)
        if i == 0:
            m = float(listed[0])
            w = float(listed[1])
            t = float(listed[2])
            r = float(listed[3])
            mas_disc = float(listed[4])
            general.append([m, w, t])

        elif i == 9:
            w0 = float(listed[0])
            t0 = float(listed[1].rstrip())
            tab[15, 2]['text'] = '\u03C90 = '.translate(SUB) + str(w0)
            tab[15, 3]['text'] = '\u03C40 = '.translate(SUB) + str(t0)
            tab[15, 4]['text'] = 0
            MM = Momentul_fortei_disc(t0, Momentum_J(mas_disc, r), w0)
            tab[15, 5]['text'] = '\U0001D440 = {:.3f}'.format(MM) # M

        else:
            m = float(listed[0])
            w = float(listed[1])
            t = float(listed[2].rstrip())
            general.append([m, w, t])

    print('general  -- ', general)
    # raza configs
    ra['text'] = 'Raza = {:.2f}(m)'.format(r)
    mass['text'] = 'Masa discului = {:.2f}(kg)'.format(mas_disc)
    mass.config(width=20)
    masa_discului.grid_forget()
    eps_r.grid_forget()
    eps_m.grid_forget()

    ra.config(width=14)
    raza.grid_forget()
    print(FrictionF_list)

    # completez tabelul
    s = 6
    for i in range(0, 9):
        tab[s, 1]['text'] = '{:.2f}'.format(general[i][0]) # masa
        tab[s, 2]['text'] = '{:.2f}'.format(general[i][1]) # w0
        tab[s, 3]['text'] = '{:.2f}'.format(general[i][2]) # tau_0
        tab[s, 4]['text'] = '{:.3f}'.format(Normal_force(general[i][0])) # F(N)
        s += 1
        normalF_list.append(Normal_force(general[i][0]))

    J = Momentum_J(mas_disc, r)
    print(J)
    print('tau_0', t0)
    for i in range(9):
        tau_current = general[i][2]
        print('tau curent', tau_current)
        Friction = Friction_force(J, w0, r,t0, tau_current)
        FrictionF_list.append(Friction)

    # forta de frecare coloana
    j = 0
    for i in range(6, 15):
        tab[i, 5]['text'] = '{:.4f}'.format(FrictionF_list[j])
        j += 1


    # completez tabelul cu coeful de frecare
    for i in range(9):
        k = Coeficient(FrictionF_list[i], normalF_list[i])
        coefs.append(k)
    j = 0
    for i in range(6, 15):
        tab[i, 6]['text'] = '{:.4f}'.format(coefs[j])
        j += 1
    tab[15, 6]['text'] = '\U0001D458 = 0'
    tab[15, 4]['text'] = '\U0001D441 = 0' # N

    # aranjam butoanele
    add.grid_configure(row=2, column=3, padx=(5, 0), pady=1)
    add.config(width=20)
    clearf.grid_configure(row=3, column=3, padx=(5, 0), pady=1)
    clearf.config(width=20)
    restart.grid_configure(row=4, column=3, padx=(5, 0), pady=1)
    restart.config(width=20)
    eps_common.grid(row=2, column=4, padx=(5, 0), pady=1)


    # plot the data
    def Show_the_plot(normalF_list, FrictionF_list):
        plt.plot(normalF_list, FrictionF_list, 'b')
        plt.plot(normalF_list, FrictionF_list, 'ro')
        plt.grid()
        plt.xlabel('Forta N')
        plt.ylabel('Forta Fᶠ')
        plt.title('Graficul dependente Fᶠ = f(N)')
        plt.show()

    # afisam erorile
    find_error(general, FrictionF_list, t0, J, r, mas_disc)
    # afisam graficul
    Show_the_plot(normalF_list, FrictionF_list)


def Export_to_Spreadsheet():
    global FrictionF_list, general, normalF_list, last, ra, raza, add, tab, coefs, r, t0, w0, mas_disc, mass, normalF_list, MM

    gc = gspread.service_account(filename='creds.json')
    sheet = gc.open_by_key('16N4bwf-u3qa4YaNsvx_s8P-zRuJH80KUe--WP5uIY98')
    worksheet = sheet.sheet1

    worksheet.insert_row(['Masa (kg)', 'Viteza Unghiulara (s^-1)', 'Timpul de oprire \u03C4 (s)', 'Forta Normala (N)', 'Forta de frecare Fᶠ (N)', 'Coeficientul de frecare'], 1)
   # worksheet.insert_row(['Parametrii Discului-->', 'Masa discului', 'Raza discului'], 1)
   # worksheet.update_cell(8, 2, mas_disc),  # ( row, column, new value )
    #worksheet.update_cell(9, 2, 28),  # ( row, column, new value )
    # Scriem datele in spreadsheet
    for i in range(9):
        vals = general[i] + [normalF_list[i], FrictionF_list[i], coefs[i]]
        worksheet.append_row(vals)
    # ultimul rand in spreadsheet
    vals = ['m = 0', '\u03C90 = '.translate(SUB) + str(w0), '\u03C40 = '.translate(SUB) + str(t0), '\U0001D441 = 0', '\U0001D440 = {:.3f}'.format(MM), '\U0001D458 = 0']
    worksheet.append_row(vals)
    ########################################################################
# ...................................  FRONT ..........................#
########################################################################


#  ------------------------------------INTRO --------------------------#
def intro():
    root1 = Tk()
    root1.title("Intro experiment")
    root1.geometry('800x720+400-80')
    root1.iconbitmap(r'cat.ico')

    root1.resizable(0, 0)
    scrollbar = Scrollbar(root1)
    scrollbar.pack(side=RIGHT, fill=Y)
    textbox = Text(root1, width = 70, height=30)
    textbox.pack()

    textbox.config(font=('Times', 16))
    textbox.insert(END, '                                             INTRODUCERE EXPERIMENT !\n\n')

    textbox.insert(END, '   Forța de frecare la alunecare aplicată pe un timp t poate fi ușor determinată având un disc \n'
                        'mobil. Instalația constă dintr-un disc masiv conectat la un motor electric, un element de \n'
                        'frânare (reprezentat prin segmentul OA) pe care pot fi aplicate diferite greutăți. Astfel, poate \n'
                        'fi modificată forța de presiune normală a frânei asupra discului (N). Această forță este direct \n'
                        'proporțională cu forța de frecare F, care se determină experimental:')

    img0 = PhotoImage(file = "0.gif")
    textbox.image_create(END, image = img0)
    textbox.insert(END, '\n\n                                              ')

    # attach textbox to scrollbar
    img = PhotoImage(file = "1.gif")
    textbox.image_create(END, image = img)

    textbox.insert(END, '\n (Figura 1. Schema instalației experimentale pentru determinare coeficientului de frecare)\n\n'
                        'Ecuația fundamentală a rotației rigidului face legătura dintre accelerația mișcării de rotație, \n'
                        'momentul de inerție în raport cu axa de rotație, și momentul forțelor exterioare în raport cu \n'
                        'această axă. În cazul instalației din figura 1, în prima aproximație poate fi considerate ca \n'
                        'forță exterioară doar forța de frecare dintre disc și frână. Totuși, pentru calcule mai precise, \n'
                        'este necesar de a ține cont și de forța de frecare în rulmenți. Respectiv ecuația mișcării de \n'
                        'rotație a discului este:')

    img2 = PhotoImage(file = "2.gif")
    textbox.image_create(END, image = img2)


    textbox.insert(END, '\nUnde: J - Momentul de inerție, R - raza discului, ω – viteza unghiulară a discului, \n'
                        'F – forța de frecare dintre disc și suport, M – momentul forței de frecare în axa cilindrului \n'
                        'și t – timpul. Considerând discul omogen, vom calcula momentul J după formula:\n                                                   ')

    img3 = PhotoImage(file = "3.gif")
    textbox.image_create(END, image = img3)

    textbox.insert(END, '\nViteza ungiulară o determinam cu ajutorul tahometrului cu curenți turbionari sau cu \n'
                        'ajutorul tahometrului bazat pe Arduino. Integrând ecuația mișcării de rotație a discului\n'
                        'în limitele 0, τ și ω0 , 0, vom obține: ')

    img4 = PhotoImage(file = "4.gif")
    textbox.image_create(END, image = img4)

    textbox.insert(END, '                                       (**)')

    textbox.insert(END, '\nUnde ω0 este viteza unghiulară inițială iar τ este timpul de oprire deplină a discului. \n'
                        'Fără aplicarea suportului pe disc (F = 0), frânarea discului va fi determinată de frecarea \n'
                        'în rulmenți și, în acest caz, timpul τ0 de  oprire totală a scripetelui (de la viteza inițială ω0)\n'
                        'este:')

    img5 = PhotoImage(file = "5.gif")
    textbox.image_create(END, image = img5)

    textbox.insert(END, '\nDesigur, M poate fi interpretat în general ca momentul forțelor exterioare restul decât \n'
                        'forța de frecare cercetată. Calculul acestor forțe poate prezenta destule dificultăți, mai \n'
                        'ales dacă considerăm că forța de rezistență a aerului depinde de mai mulți factori, inclusiv \n'
                        'viteza discului. Formula precedentă permite de a determina direct acest moment M prin \n'
                        'cronometrarea timpului de oprire a discului atunci când frâna este scoasă.')

    img6 = PhotoImage(file = "6.gif")
    textbox.image_create(END, image = img6)

    textbox.insert(END, '\nRevenind la ecuația (**), putem deduce expresia pentru forța de frecare dintre disc și frână:\n'
                        '                                                 ')

    img7 = PhotoImage(file = "7.gif")
    textbox.image_create(END, image = img7)


    on_click = "#e2f1f8"
    txt_color = "#000000"

    # distrugem intro page si trecem la main page
    def foo():
        root1.destroy()

    # iesim din program
    def foo1():
        root1.destroy()
        exit()
    # butoanele
    submit = Button(root1, text="Start Experiment", font="Times 14", width=20, bg='#9CE39B', fg=txt_color,
                    activebackground=on_click, command=foo)
    submit.pack(side=LEFT, padx=(100,0))

    close = Button(root1, text="Close", font="Times 14", width=20, bg='#EF9898', fg=txt_color,
                    activebackground=on_click, command=foo1)
    close.pack(side=RIGHT, padx=(0,100))

    textbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=textbox.yview)

    root1.mainloop()


# ----------------------------------- MAIN ----------------------------#
# Intro Page first
#intro()

# Color Schemes
top_block = "#b0bec5"
highlight_backg = top_block
txt_color = "#000000"
alg_color = txt_color
ufo = "#cfd8dc"
bg_alg = ufo
on_click = "#e2f1f8"
entry_color = "#eceff1"
buttons_color = "#eeeeee"
add_color_btn = '#D5F2D1'
clear_fields_color_btn = '#F2DEA7'
submit_color_btn = '#7CE596'
restart_corol_btn = '#F2BBA7'


# Main Root config
root = Tk()
root.title("PBL 2")
root.geometry('919x775+300-40')
root.configure(bg=ufo)
root.resizable(0, 0)
root.iconbitmap(r'cat.ico')

# Menu ( Import )
main_menu = Menu(root)
root.configure(menu=main_menu)

first_item = Menu(main_menu, tearoff=0, background=ufo, foreground='#000000', activebackground='#eeeeee',
                  activeforeground='#000000')

main_menu.add_cascade(label="Menu", menu=first_item)
first_item.add_command(label="Import data from Txt", command=Import_data)
first_item.add_command(label="Import data from Spreadsheets", command=Import_data_Spreadsheets)
first_item.add_command(label="Export to Spreadsheets", command=Export_to_Spreadsheet)

# For Subscription equations
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

# FRAME 1 ..................................... FOOTER  ............................

frame1 = Frame(root, bg=ufo, highlightbackground=highlight_backg, )
frame1.grid(row=0, sticky=NSEW)

footer = Label(frame1, text="Determinarea experimentală a coeficientului de frecare la alunecare", font="Times 16 bold",
               bg=top_block, relief=RAISED, fg=txt_color, width=75)
footer.grid(pady=(2, 20), padx=(4, 0))

# FRAME 2 ..................................... CURRENT  ............................
frame2 = Frame(root, bg=ufo, highlightbackground=highlight_backg, highlightthickness=2, width=70)
frame2.grid(row=1, columnspan=6, sticky=NSEW)

masal = Label(frame2, text="Masa curentă (kg): ", font="Times 16 bold", bg=top_block, relief=RAISED, fg=txt_color)
masal.grid(row=1, column=0, pady=2, padx=2)
masa = Entry(frame2, font=14, width=16, bg=entry_color, fg=txt_color)
masa.grid(row=2, column=0, pady=2, padx=2, sticky=W)

v = Label(frame2, text="Viteza \u03C90 (s⁻¹): ".translate(SUB), font="Times 16 bold", bg=top_block, relief=RAISED,
          fg=txt_color)
v.grid(row=1, column=1, pady=2, padx=2)
viteza = Entry(frame2, font=14, width=12, bg=entry_color, fg=txt_color)
viteza.grid(row=2, column=1, pady=2, padx=(2, 2))

t = Label(frame2, text="Timpul \u03C4 (s): ".translate(SUB), font="Times 16 bold", bg=top_block, relief=RAISED,
          fg=txt_color, width=10)
t.grid(row=1, column=2, pady=2, padx=2)
tau = Entry(frame2, font=14, bg=entry_color, fg=txt_color, width=11)
tau.grid(row=2, column=2, pady=2, padx=(1, 1))

plot_btn = Button(frame2, text="Plot the graph 📈", font="Times 11", width=20, bg=submit_color_btn, fg=txt_color,
                      activebackground=on_click)

ra = Label(frame2, text="Raza discului (m):", font="Times 16 bold", width=15, bg=top_block, relief=RAISED, fg=txt_color)
ra.grid(row=1, column=3, pady=1, padx=2)
raza = Entry(frame2, font=16, width=16, bg=entry_color, fg=txt_color)
raza.grid(row=3, column=3, pady=1, padx=(5,2))

eps_r = Label(frame2, text="ε(R) = \u00B10,005 (m) ", font="Times 14", bg=ufo, fg=txt_color)
eps_r.grid(row=2, column=3, padx=(5, 0))

mass = Label(frame2, text="Masa discului (kg): ".translate(SUB), width=16, font="Times 16 bold", bg=top_block, relief=RAISED, fg=txt_color)
mass.grid(row=1, column=4, pady=1, padx=2)
masa_discului = Entry(frame2, font=16, width=17, bg=entry_color, fg=txt_color)
masa_discului.grid(row=3, column=4, pady=1, padx=(0,2))

eps_m = Label(frame2, text="ε(m) = \u00B10,005 (kg) ", font="Times 14", bg=ufo, fg=txt_color)
eps_m.grid(row=2, column=4, padx=(5, 0))

eps_common = Label(frame2, text="ε = \u00B10,005 (kg,m) ", font="Times 14", bg=ufo, fg=txt_color)

add = Button(frame2, text="Add values & Solve ✚", font="Times 11", width=20, bg=add_color_btn, fg=txt_color,
             activebackground=on_click)
add.grid(row=4, column=3, padx=(5, 0))
clearf = Button(frame2, text="Clear fields ✗", font="Times 11", width=20, bg=clear_fields_color_btn, fg=txt_color,
                activebackground=on_click, command=clear_fields)

info = Label(frame2, text="Pentru masa = 0 :", font="Times 14", bg=top_block, relief=RAISED, fg=txt_color)
info.grid(row=3, column=0, rowspan=2, pady=(5, 2), padx=4, sticky=NSEW)

v0 = Label(frame2, text="Viteza \u03C90 (s⁻¹): ".translate(SUB), font="Times 16 bold", bg=top_block, relief=RAISED,
           fg=txt_color)
v0.grid(row=3, column=1, pady=(5, 1), padx=2)
viteza0 = Entry(frame2, font=14, width=12, bg=entry_color, fg=txt_color, state=DISABLED)
viteza0.grid(row=4, column=1, padx=0, pady=(1, 0))

t0 = Label(frame2, text="Timpul \u03C40 (s): ".translate(SUB), font="Times 16 bold", bg=top_block, relief=RAISED,
           fg=txt_color)
t0.grid(row=3, column=2, pady=(5, 1), padx=2)
tau0 = Entry(frame2, font=14, width=11, bg=entry_color, fg=txt_color, state=DISABLED)
tau0.grid(row=4, column=2, padx=0, pady=(1, 0))

submit = Button(frame2, text="Submit (Plot) ✓", font="Times 11", width=20, bg=submit_color_btn, fg=txt_color,
                activebackground=on_click, state=DISABLED)

restart = Button(frame2, text="Restart Experiment ⟲", font="Times 11", width=20, bg=restart_corol_btn, fg=txt_color,
                 activebackground=on_click)
restart.grid(row=4, column=4, padx=(5, 0), pady=(1, 1))

nota_label = Label(frame2, font="Times 14 bold", bg=ufo, fg=txt_color, width=89)
nota_w0 = Label(nota_label, text='NOTA ❕    \u03C90 - viteza unghiulară inițială al discului (se masoară în momentul întreruperii curentului in motor),'.translate(SUB),
                 font='Times 14',bg=ufo, fg=txt_color)
nota_tau = Label(nota_label, text='\u03C4 - timput de oprire al discului (după ce întrerupem curentul în motor, pornim cronometrul și \nsalvăm timpul la '
                                  'oprirea deplină a discului adică \u03C90'.translate(SUB) + ' = 0).',
                 font='Times 14',bg=ufo, fg=txt_color)
nota_label.grid(row=5,rowspan=4, columnspan=10, sticky=NSEW)

nota_w0.grid(columnspan=10 ,sticky=NSEW)
nota_tau.grid(column=8 ,sticky=NSEW)

# ............................................ TABEL FOOTER ............................
ftab = Frame(root, bg=ufo, highlightbackground=highlight_backg)
ftab.grid(row=2, columnspan=6, sticky=W, padx=(4, 0))
t = Label(ftab, text='Tabelul Datelor', font="Times 16 bold", bg=top_block, relief=SUNKEN, fg=txt_color, width=75)
t.grid(row=2, sticky=NSEW, pady=(15, 2), columnspan=5)

# FRAME 3 ..................................... TABEL DATA ..............................
frame3 = Frame(root, bg=ufo, highlightbackground=highlight_backg, highlightthickness=2, width=75)
frame3.grid(row=3, sticky=W, padx=(4, 0))

# creez tabelul de label-uri pentru a putea fi modificate anterior
tab = dict()
for i in range(5, 16):
    for j in range(7):
        txt = '      '
        tab[i, j] = Label(frame3, text=txt, font="Times 14", bg="white", relief=RAISED, fg=txt_color, width=13)
        tab[i, j].grid(row=i, column=j)
        if i == 5:
            tab[i, j].config(height=2)

# notez valorile in tabel
tab[5, 0]['text'] = "Nr. de \nîncercări"
tab[5, 0].config(width=8)
tab[5, 1]['text'] = 'Masa (kg)'
tab[15, 1]['text'] = 'masa = 0 '
tab[15, 2]['text'] = '\u03C90 =__'.translate(SUB)
tab[15, 3]['text'] = '\u03C40 =__'.translate(SUB)
tab[15, 4]['text'] = '\U0001D441 = 0' # N
tab[15, 5]['text'] = '\U0001D440 =__'.translate(SUB) # M
tab[15, 6]['text'] = '\U0001D458 = 0'

tab[5, 2]['text'] = 'Viteza\nunghiulară \u03C90(s⁻¹)'.translate(SUB)
tab[5, 3]['text'] = 'Timpul de\n oprire \u03C4 (s)'.translate(SUB)
tab[5, 4]['text'] = 'Forța\n normală \U0001D441 (N)'.translate(SUB)
tab[5, 5]['text'] = 'Forța \nde frecare - Fᶠ(N)'.translate(SUB)
tab[5, 6]['text'] = 'Coeficientul \nde frecare \U0001D458'.translate(SUB)

# indexam randurile taelului ( Nr de incercari )
c1 = 1
for i in range(6, 16):
    tab[i, 0]["text"] = c1
    tab[i, 0].config(width=8)
    c1 += 1

# nota pentru M ( momentul forței de rezistenta)
momentul_M = Label(frame3, font="Times 14", bg=ufo, fg=txt_color, width=89)
mom_M = Label(momentul_M, text='NOTA ❕   \U0001D440 este momentul de rezistență.', font='Times 14',bg=ufo, fg=txt_color )
momentul_M.grid(row=20, columnspan=10, sticky=W)
mom_M.grid()

# ......................................... ERORI FOOTER............................
er = Frame(root, bg=ufo, highlightbackground=highlight_backg)
er.grid(row=4, columnspan=6, sticky=W, padx=(4, 0))
errori = Label(er, text='Calculul Erorilor', font="Times 16 bold", bg=top_block, relief=SUNKEN, fg=txt_color, width=75)
errori.grid(row=4, sticky=NSEW, columnspan=5, pady=(15, 2))

# FRAME 4 ..................................... EROORI DATA ..............................
frame4 = Frame(root, bg=ufo, highlightbackground=highlight_backg, highlightthickness=2, relief=SUNKEN, width=75, height=60)
frame4.grid(row=5, columnspan=6, sticky=NSEW, padx=(4, 0))

delta_m = Label (frame4, text='Δ\U0001D45A = 0.005', font="Times 17", bg=ufo, fg=txt_color)
delta_m.grid(row=0, column=0)
delta_R = Label(frame4, text='| Δ\U0001D493 = 0.005', font="Times 17", bg=ufo, fg=txt_color)
delta_R.grid(row=0, column=1)
delta_w = Label(frame4, text='| Δ\u03C9 = 0.05', font="Times 17", bg=ufo, fg=txt_color)
delta_w.grid(row=0, column=2)
delta_tau = Label(frame4, text='| Δ\u03C4 = 0.5', font="Times 17", bg=ufo, fg=txt_color)
delta_tau.grid(row=0, column=3)

delta_ff = Label(frame4, text='| ΔFᶠ = ___', font="Times 17", bg=ufo, fg=txt_color)
delta_ff.grid(row=0, column=4)
eps = Label(frame4, text='| \U0001D700 = ___%', font="Times 17", bg=ufo, fg=txt_color)
eps.grid(row=0, column=5)

# Comenzile pentru butoanele pricipale
add.bind("<Button-1>", add_val)
restart.bind("<Button-1>", Restart_experiment)
submit.bind("<Button-1>", Plot_the_graph)

root.mainloop()
# Check commit github