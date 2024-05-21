clear
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Global_controller_1\"
load(folder+'Global_compaison.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Distributed_system_6\"
load(folder+'ADMM_compaison.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Simulation\"
load(folder+ 'global_controller_465_mm.mat')
close all

f = figure('Position',[10 10 900 600/2])
tiledlayout(1,2, "TileSpacing","compact")
nexttile
plot(0:99,Volume(1:100)*1000)
hold on
plot(Global.tower_vol_time, Global.tower_vol)
plot(ADMM.tower_vol_time,ADMM.tower_vol)

yline(28)
yline(155)
ylabel("Volume in tower [L]")
xlabel('Time [h_a]')
ylim([20 170])
xlim([0 100])
grid 

nexttile
stairs(0:99,summedMassflow(1:100))
hold on
plot(Global.flow_time, Global.flow)
plot(ADMM.flow_time,ADMM.flow)
ylabel('Commanded sum of flows [m^3/h]')
xlabel('Time [h_a]')
ylim([0 0.6])
xlim([0 100])
grid

fontname(f,"Times")

legend("Simulation", "Global controller", "Privacy-pre. controller")
exportgraphics(f, 'comparison.pdf')
 
