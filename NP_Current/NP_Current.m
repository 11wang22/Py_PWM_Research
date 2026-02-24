clc,clear

%%% system variable parameters
Modulation = 0:1e-3:2 / sqrt(3); 
wt = 0:1e-3:2 * pi / 3;
[X,Y] = meshgrid(Modulation,wt);
[Lenx,Leny] = size(X);
Y = Y * 180 / pi;

%%% three-phase voltage
Ua  = zeros(Lenx,Leny);
Ub  = zeros(Lenx,Leny);
Uc  = zeros(Lenx,Leny);
Umax = zeros(Lenx,Leny);
Umin = zeros(Lenx,Leny);

for i = 1:Lenx
    for j = 1:Leny
        Ua(i,j) = Modulation(j) * sin(wt(i));
        Ub(i,j) = Modulation(j) * sin(wt(i) - 2 * pi / 3);
        Uc(i,j) = Modulation(j) * sin(wt(i) + 2 * pi / 3);

        Umax(i,j) = max([Ua(i,j) Ub(i,j) Uc(i,j)]);
        Umin(i,j) = min([Ua(i,j) Ub(i,j) Uc(i,j)]);
    end
end

%%% zero-sequence voltage limitation
Uzsmax  = zeros(Lenx,Leny);
Uzsmin  = zeros(Lenx,Leny);
for i = 1:Lenx
    for j = 1:Leny
        Uzsmax(i,j) = min([(1 - Umax(i,j)) -Umin(i,j)]);
        Uzsmin(i,j) = max([(-1 - Umin(i,j)) -Umax(i,j)]);
    end
end

%%% 科研绘图设置
% 设置全局字体和线条属性
set(groot, 'defaultAxesFontName', 'Times New Roman');
set(groot, 'defaultAxesFontSize', 14);
set(groot, 'defaultLineLineWidth', 1.5);

% 创建图形窗口
figure();

% 绘制曲面
% 上边界 Uzs_max
h1 = surf(X, Y, Uzsmax, ...
         'FaceColor', [245/255 117/255 85/255], ...
         'EdgeColor', 'none', ...
         'FaceAlpha', 0.6);
hold on;
grid on;

% 下边界 Uzs_min
h2 = surf(X, Y, Uzsmin, ...
         'FaceColor', [252/255 199/255 150/255], ...
         'EdgeColor', 'none', ...
         'FaceAlpha', 0.6);

% 添加等高线以增强趋势显示
contour3(X, Y, Uzsmax, 20, ...
         'Color', [245/255 117/255 85/255], ...
         'LineWidth', 1.5);
contour3(X, Y, Uzsmin, 20, ...
         'Color', [252/255 199/255 150/255], ...
         'LineWidth', 1.5);
