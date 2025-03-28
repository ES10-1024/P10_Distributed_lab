clear
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Global_controller_2\"
load(folder+'Global_compaison.mat')
folder = "C:\Users\laula\OneDrive - Aalborg Universitet\10. semester\Log_files\Distributed_system_7\"
load(folder+'ADMM_compaison.mat')
close all
%%
close all

%Claculate predicted flow global simulation

[~,idx] = min(abs(Global.tower_vol_time/600-79))

f = figure('Position',[10 10 900 350])
tiledlayout(4,1, "TileSpacing","tight")
nexttile
stairs(0:79,Global.El_price(1:80))
hold on
stairs(79:100,Global.El_price(80:101))
xlim([0 100])

ylabel('Electricity price [EUR/kWh]')
get(gca)
set(gca,'YAxisLocation','right')
grid


nexttile

p3=plot(ADMM.tower_vol_prediction1_time, ADMM.tower_vol_prediction2, LineWidth=4)   %ADMM pred
hold on
p5=plot(Global.tower_vol_prediction_time, Global.tower_vol_prediction, Linewidth=1.5) %Global pred

p4=plot(ADMM.tower_vol_time,ADMM.tower_vol, LineWidth=4)
p6=plot(Global.tower_vol_time(1:idx)/600, Global.tower_vol(1:idx),Linewidth=1.5)

xlim([0 100])
yline(28)
yline(155)
ylabel(["Volume in tower [L]";"Meas. / pred."])
ylim([20 170])
xlim([0 100])
grid 
nexttile

hold on
stairs(ADMM.flow_prediction1_time(1:end-1),ADMM.flow_prediction2, LineWidth=4)
stairs(Global.flow_prediction_time(1:end-1), Global.flow_prediction, Linewidth=1.5)
%Predictions
stairs(ADMM.flow_time,ADMM.flow, LineWidth=4)
stairs(Global.flow_time, Global.flow, Linewidth=1.5)

ylabel({"Sum of flows [m^3/h]";"Act. / pred." })

ylim([0 0.6])
xlim([0 100])
grid
get(gca)
set(gca,'YAxisLocation','right')

nexttile
xlabel('Time [h_a]')
p2=stairs(Global.consumption_time, Global.consumption)
hold on
p1=stairs(Global.consumption_pred, Global.consumption_pred_time)
xlim([0 100])
ylabel(['Consumption [m^3/h]';"Act. / pred."])
grid
xlabel('Time [h_a]')




lgd = legend([p1 p2 p3 p4 p5 p6],"Prediction both", "Actuation/measurements both","Privacy-preserving controller prediction", "Privacy-preserving controller actuation/measurement","Centralised controller prediction", "Centralised controller actuation/measurement", 'Orientation','vertical', 'NumColumns',3)




fontname(f,"Times")

%lgd = legend("PPC pred. pump 2",  "GC pred.", "Sim GC pred.", "PPC mea/cmd", "GC mea/cmd" , "Sim GC cmd", 'Orientation','Horizontal')

lgd.Layout.Tile = 'south';
f.Renderer='Painters';
exportgraphics(f, 'comparison.pdf')


 
