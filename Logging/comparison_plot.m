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

volume_pred = ModelPredicted(Volume(79),simData.logsout{2}.Values.Data(80,:)',simData.logsout{4}.Values.Data(:,:,80))*1000
[~,idx] = min(abs(Global.tower_vol_time/600-79))

f = figure('Position',[10 10 900 600/2])
tiledlayout(2,1, "TileSpacing","compact")
nexttile
plot(ADMM.tower_vol_prediction1_time, ADMM.tower_vol_prediction2)
hold on
plot(Global.tower_vol_prediction_time, Global.tower_vol_prediction)
plot(79:79+23, volume_pred)
plot(ADMM.tower_vol_time,ADMM.tower_vol)
plot(Global.tower_vol_time(1:idx)/600, Global.tower_vol(1:idx))
plot(0:79,Volume(1:80)*1000)



  
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

%lgd = legend("PPC pred. pump 2",  "GC pred.", "Sim GC pred.", "PPC mea/cmd", "GC mea/cmd" , "Sim GC cmd", 'Orientation','Horizontal')
lgd = legend("Privacy-preserving controller prediction pump 2",  "Global controller prediction", "Simulated global controller prediction", "Privacy-preserving controller measured/commanded", "Global controller measured/commanded" , "Simulated global controller commanded", 'Orientation','Horizontal', 'NumColumns',3)
lgd.Layout.Tile = 'south';
f.Renderer='Painters';
exportgraphics(f, 'comparison.pdf')
 
