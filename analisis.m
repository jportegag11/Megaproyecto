fileID = fopen('atitlan25-08-18_2_nogps_2018_04_28_05h00.dat','r');
for i = 1:42
    fgetl(fileID);
end
linea = fgetl(fileID);
datos = zeros(1,567665);
for k = 1:567665
    pulso = 0;
    prueba = fgetl(fileID);
    num = str2double(prueba(1));
    while (isnan(num))
        prueba = fgetl(fileID);
        num = str2double(prueba(1));
    end
    muestra = str2double(prueba(7:end));
    pulso = pulso + muestra -50;
    for j = 1:11
        linea = fgetl(fileID);
        muestra = str2double(linea(7:end));
        pulso = pulso + muestra -50;
    end
    datos(k) = pulso;
end
fclose(fileID);
largo = length(unique(datos));
histogram(datos,largo);
%ylim([0 5]);