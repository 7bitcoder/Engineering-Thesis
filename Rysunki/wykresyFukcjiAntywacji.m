clear all;
close all;
x = [-5 5];
liniowa = @(x) 2*x;
pliniowa = @(x) 2;
progowa = @(x) heaviside(x);
pprogowa = @(x) dirac(x);
sigmoidalna = @(x) 1/(1+ exp(-x));
psigmoidalna = @(x) exp(-x)/((1+ exp(-x))^2);
relu = @(x) max(0,x);
prelu = @(x) heaviside(x);
subplot(2,2,1)
fplot(liniowa,x,'LineWidth',1.5)
hold on 
fplot(pliniowa,x,'LineWidth',1)
grid on
title('Funkcja Liniowa')
subplot(2,2,2)
fplot(progowa,x,'LineWidth',1.5)
hold on 
ff = -5:0.01:5
y = double(ff == 0);
plot(ff, y,'LineWidth',1);
grid on
title('Funkcja Progowa')
subplot(2,2,3)
fplot(sigmoidalna,x,'LineWidth',1.5)
hold on 
fplot(psigmoidalna,x,'LineWidth',1)
grid on
title('Funkcja Sigmoidalna')
subplot(2,2,4)
fplot(relu,x,'LineWidth',1.5)
hold on 
fplot(prelu,x,'LineWidth',1)
grid on
title('Funkcja Relu')
legend('funkcja aktywacji','pochodna funkcji aktywacji')