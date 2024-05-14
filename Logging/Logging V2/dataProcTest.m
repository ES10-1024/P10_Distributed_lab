%% 
clear 
clc 
clf 
close all 

%% Function to pick out the desired IDs from the log file 
%Input filename, the file it is desired to work with, including .csv! 
%IDlabels for the matrix to be create 
%groupNumber, tells which ID is present i which row 
%Output log, returns a struct with the data and sampling time
addpath('C:\Users\is123\Downloads\Distributed_system_3\Distributed_system_3')
%filename='ADMM1_05-09_12-54-40.csv';
filename='pump1_05-14_13-57-56.csv';
%filename='return_and_consumer_valve_ctrl_05-09_12-54-42.csv';
%%

opts = detectImportOptions(filename);

opts.VariableTypes = {'string', 'string', 'double'}; 

data = readtable(filename, opts);

% Creating names for the matrices
[IDLabels, ~,groupNumber] =unique(data.ID); 

%Replacing space with _ in naming
for i = 1:numel(IDLabels)
    IDLabels{i} = strrep(IDLabels{i}, ' ', '_');
end

%% Setting up paralle work and getting the amount of works
try
    parpool();
end 

% Get the current parallel pool object
currentPool = gcp();

% Get the number of workers in the pool
numWorkers = currentPool.NumWorkers;
%% Splliting the data up to the amount of workers presented. 

startline=1; 
TotalSize=size(data,1); 
EachHave=floor(TotalSize/numWorkers); 
for index=1:numWorkers-1
    endline(index,1)=EachHave*index; 
    startline(index+1,1)=startline(index,1)+EachHave;
end 
endline(numWorkers,1)=TotalSize; 

%% Getting the data form the logge files 
% Initialize an empty cell array to store the output structures
outputStructs = {};

tic 
parfor i = 1:numWorkers
    outputStructs{i} = logProc(data(startline(i,1):endline(i,1),:), IDLabels, groupNumber(startline(i,1):endline(i,1),1));
end
toc

%% Combine the output structures into a single structure
combinedStruct = struct();
for i = 1:numWorkers
    combinedStruct = mergeStructs(combinedStruct, outputStructs{i});
end



%% The rest is functions!!!!!! 


% Function to merge two structures as columns
function mergedStruct = mergeStructs(struct1, struct2)
    mergedStruct = struct1;
    fields = fieldnames(struct2);
    for j = 1:numel(fields)
        field = fields{j};
        if isfield(mergedStruct, field)
            % Transpose the field from struct2 and concatenate it as a column
            mergedStruct.(field) = [mergedStruct.(field), struct2.(field)];
        else
            % Create a new field in mergedStruct
            mergedStruct.(field) = struct2.(field);
        end
    end
end
