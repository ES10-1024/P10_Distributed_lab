clear
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Global_controller_1\"
load(folder+'Global_compaison.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Distributed_system_7\"
load(folder+'ADMM_compaison.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Simulation\"
load(folder+ 'global_controller_465_mm.mat')
close all
%%
close all

%Claculate predicted flow global simulation
flow_pred_sim = simData.logsout{2}.Values.Data(80,1:2:end) + simData.logsout{2}.Values.Data(80,2:2:end)


f = figure('Position',[10 10 900 600/2])
tiledlayout(2,1, "TileSpacing","compact")
nexttile
%plot(ADMM.tower_vol_time,ADMM.tower_vol)
hold on
[~,idx] = min(abs(Global.tower_vol_time/600-79))
%plot(Global.tower_vol_time(1:idx)/600, Global.tower_vol(1:idx))
%plot(0:79,Volume(1:80)*1000)

%plot(ADMM.tower_vol_prediction1_time, ADMM.tower_vol_prediction2)
%plot(Global.tower_vol_prediction_time, Global.tower_vol_prediction)
plot(79:79+24,[simData.logsout{3}.Values.Data(79)*0.283, simData.logsout{3}.Values.Data(79)*0.283+flow_pred_sim/6*1000-simData.logsout{5}.Values.Data(80:80+23)'/6*1000  ])


  
xlim([0 100])




yline(28)
yline(155)
ylabel("Volume in tower [L]")
xlabel('Time [h_a]')
ylim([20 170])
xlim([0 100])
grid 

nexttile

hold on
stairs(ADMM.flow_prediction1_time(1:end-1),ADMM.flow_prediction2)
stairs(Global.flow_prediction_time(1:end-1), Global.flow_prediction)

stairs((2:24)+77,flow_pred_sim(2:24))

%Predictions
stairs(ADMM.flow_time,ADMM.flow)
stairs(Global.flow_time, Global.flow)
stairs(0:79,summedMassflow(1:80))
ylabel('Sum of flows [m^3/h]')
xlabel('Time [h_a]')
ylim([0 0.6])
xlim([0 100])
grid

fontname(f,"Times")

lgd = legend("PPC pred. pump 2",  "GC pred.", "Sim GC pred.", "PPC Mes/CMD", "GC Mes/CMD" , "Sim GC CMD", 'Orientation','Horizontal')
lgd.Layout.Tile = 'south';
exportgraphics(f, 'comparison.pdf')
 
