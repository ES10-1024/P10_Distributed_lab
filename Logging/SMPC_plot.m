%What do i need to plot



%Something where smpc has not been appiled
%The first entry in s_z_i and the first entry in S_z
%Plot send z_i
%Plot recived z_i


%Something where smpc has been applied
%Plot send shares to s2
%Plot recived shares from s2
%Plot sum of shares from s2
%Plot sum of shares to s2
%%
folder = "C:\Users\laula\Documents\GitHub\P10_Distributed_lab\Logging\Log_files\"
smpc = dataProc(folder+'smpc1_05-23_11-36-39.csv')
no_smpc = dataProc(folder + 'ADMM1_05-23_11-36-39.csv')
%% Plot of send smpc data
close all 
f = figure
tiledlayout(2,1,"TileSpacing","compact")
nexttile
plot(smpc.b1x2(1,:),'x')
ylim([0 4294967029])
xlabel("Iteration")
grid
ylabel("Share $$s_{1,2}$$", Interpreter="latex")
nexttile
plot(smpc.b1(1,:),'x')
ylim([0 4294967029])
xlabel("Iteration")
grid
ylabel("Sum of shares $$b(1)$$", Interpreter="latex")
fontname(f,"Times")
exportgraphics(f, 'smpc_comunication.pdf')

%% Plot of send data without smpc
f = figure
plot(no_smpc.z_i(1,:),'x')
grid
xlabel("Iteration")
ylabel("First enty in $$s_{z_1}$$", Interpreter="latex")
fontname(f,"Times")
exportgraphics(f, 'no_smpc_communication.pdf')