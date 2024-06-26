function [log] = logProcces(filename)
%% Function to pick out the desired IDs from the log file 
%Input filename, the file it is desired to work with, including .csv! 
%Output log, returns a struct with the data and sampling time

opts = detectImportOptions(filename);
opts.VariableTypes = {'string', 'string', 'double'}; 

data = readtable(filename, opts);


%% Creating empty matrices for each ID 

[IDLabels, ~,groupNumber] =unique(data.ID); 

%Replacing space with _ in naming
for i = 1:numel(IDLabels)
    IDLabels{i} = strrep(IDLabels{i}, ' ', '_');
end



for i = 1:numel(IDLabels)
    eval([IDLabels{i} ' = [];']);
    eval([IDLabels{i} 'Time = [];']);
    IDLabelsTime{i}=[IDLabels{i} 'Time'];
end

%% Picking out the data for each of the IDs


    %Going though each of the entires in the sample data  
for index=1:1:size(data,1) 
        %Get the current matrix variable name based on the row
        matrixNumber = groupNumber(index,1);
        current_var_name = IDLabels{matrixNumber};
        current_var_name_Time = IDLabelsTime{matrixNumber};

        %Saving the time 
        eval([current_var_name_Time ' = [' current_var_name_Time ', data.Time(index)];']);
        %getting the data from string to double
        dataWork=str2double(data.Data(index));
        % if str2double works, save the data (if we do not get NaN or a
        % empty matrix save the data) 
        if isnan(dataWork) == 0 && isempty(dataWork) == 0
            eval([current_var_name ' = [' current_var_name ', dataWork];'])
        else 
            % Replace 'e-' with 'e-'
            str = strrep(data.Data(index), 'e-', 'e-');
            % Extract numeric values using regular expression
            %numeric_values = regexp(data.Data(index), '[-+]?\d+\.\d+', 'match');
            numeric_values = regexp(data.Data(index), '[-+]?\d+\.\d+e[-+]\d+', 'match');
            %If the data is empty or the wrong size do it another way 
            if isempty(numeric_values)==1  || ...
                     (size(numeric_values, 2) ~= 1 && ...
                    size(numeric_values, 2) ~= 2 && ...
                    size(numeric_values, 2) ~= 24 && ...
                    size(numeric_values, 2) ~= 48) 
                    %Getting the data another way!
                     numeric_values = regexp(data.Data(index), '[-+]?\d*\.?\d+', 'match');
                    %numeric_values = regexp(data.Data(index), '[-+]?\d*\.\d?', 'match');
            end 
            %If convter data from string and save it 
            if isempty(numeric_values) ==0 
                     dataWork = str2double(numeric_values)';     
                     eval([current_var_name ' = [' current_var_name ', dataWork];']);
                     % numeric_values = regexp(data.Data(index), '[-+]?\d+\.\d+', 'match');
                     % temp = str2double(numeric_values)';
                     % 
                     % eval([current_var_name ' = [' current_var_name ', temp];']); 
            else %Just add the data, noting do to it 
               eval([current_var_name ' = [' current_var_name ', data.Data(index)];']);
            end 
         end   
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

%% Making struct to hold all the important data 

for matrixNumber = 1:numel(IDLabels)
    % Get the current matrix variable name
    current_var_name = IDLabels{matrixNumber};
    current_var_name_Time = IDLabelsTime{matrixNumber};
    log.(current_var_name)=eval(current_var_name); 
    log.(current_var_name_Time)=eval(current_var_name_Time); 
end 



end

