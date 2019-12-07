clear all;
 close all;
 ff = -2:0.01:2;
a = 0.01;
leaky = []
for i = ff
    val = i;
    if i < 0
       val = a*i; 
    end
    leaky = [leaky val];
end
subplot(2,2,1)
plot(ff,leaky,'LineWidth',1.5)
hold on 
pleaky = []
for i = ff
    val = 1;
    if i < 0
       val = a; 
    end
    pleaky = [pleaky val];
end
plot(ff,pleaky,'LineWidth',1)
grid on
title('Leaky Relu')
subplot(2,2,2)
param = []
a = 0.2
for i = ff
    val = i;
    if i < 0
       val = a*i; 
    end
    param = [param val];
end
plot(ff,param,'LineWidth',1.5)
hold on 
pparam = []
for i = ff
    val = 1;
    if i < 0
       val = a; 
    end
    pparam = [pparam val];
end
plot(ff, pparam,'LineWidth',1);
grid on
title('Parametric Relu a=0.2')
subplot(2,2,3)
a = 0.2;
ELU = []
for i = ff
    val = i;
    if i < 0
       val = a*(exp(i) - 1); 
    end
    ELU = [ELU val];
end
plot(ff,ELU,'LineWidth',1.5)
hold on 
pELU = []
for i = ff
    val = 1;
    if i < 0
       val = a*(exp(i)); 
    end
    pELU = [pELU val];
end
plot(ff,pELU,'LineWidth',1)
grid on
title('ELU a = 0.2')
subplot(2,2,4)
a = 1
soft = []
for i = ff
    val =  a*log(1 +  exp(i));
    soft = [soft val];
end
plot(ff,soft,'LineWidth',1.5)
hold on 
psoft = []
for i = ff
    val =  a*exp(i)/(1 +  exp(i));
    psoft = [psoft val];
end
plot(ff,psoft,'LineWidth',1)
grid on
title('Softplus a = 1')
legend('funkcja aktywacji','pochodna funkcji aktywacji')