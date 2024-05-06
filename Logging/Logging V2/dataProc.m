function [combinedStruct] = dataProc(filename) 
%Function to pick out data from the logge files with the name filename, and return a struct with the logged data  
%Loading in data: 
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
    pool = parpool;
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

%% Setting the start time to zero, by finding the minimum timestamp
% % Initialize variables
min_value = Inf;  % Initialize to positive infinity
min_index = 0;     % Initialize to an invalid index

% Iterate through the cell array
for i = 1:numel(IDLabelsTime)
    % Get the name of the current matrix
    current_matrix_name = IDLabelsTime{i};

    % Get the value of the first entire of the current matrix
    current_value = eval([current_matrix_name '(1)']);

    % Compare the value with the current minimum
    if current_value < min_value
        min_value = current_value;  % Update minimum value
        min_index = i;               % Update index of the minimum value
    end
end

% Iterate through the cell array
for i = 1:numel(IDLabelsTime)
    % Get the name of the current matrix
    current_matrix_name = IDLabelsTime{i};
    %Strubtacting the start time
    eval([current_matrix_name ' = [' current_matrix_name '-min_value];'])
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


end
 
