obj=double(im2gray(imread('./images/cameraman.png')));
mask=padarray(ones(size(obj)),[128,128],0);
obj=padarray(obj,[128,128],0);
Fixed_Amp=abs(fft2(obj));
[h,w]=size(obj);

[~,pha,err_HIO]=fienup_phase_retrieval(Fixed_Amp,[],mask,0.8,500,"HIO");
[obj_recons,~,err_ER]=fienup_phase_retrieval(Fixed_Amp,pha,mask,0.8,100,"ER");

fig=figure;

set(fig, 'Position', [100, 100, 1200, 300]);
subplot(1,3,1)
imshow(obj,[]);
title('obj\_padded');

subplot(1,3,2)
imshow(obj_recons,[]);
title('obj\_recons');

subplot(1,3,3)
plot(log([err_HIO,err_ER]));
title('err\_convergence');
saveas(gcf, './asset/result_matlab.png');
%%
function [obj_recons,pha,err] = fienup_phase_retrieval(mag,pha,suppmat,beta,steps,mode)

if isempty(pha)
    pha=exp(1j*2*pi*rand(size(mag)));
end
err=zeros(1,steps);
y_hat=mag.*pha;
x=zeros(size(mag));
x_p=[];
    for i=1:steps
        y=real(ifft2(y_hat));
        if isempty(x_p)
            x_p=y;
        else
            x_p=x;
        end
        x=y;
      
        indices = find((y < 0 & suppmat) | (~suppmat));

        if (mode=="HIO")
            x(indices)=x_p(indices)-beta*y(indices);
        elseif (mode=="ER")
            x(indices)=0;
        end
        
        x_hat=fft2(x);
        y_hat=mag.*exp(1j*angle(x_hat));
        err(i)= immse(abs(x_hat), mag);
    end
obj_recons=x;
pha=exp(1j*angle(x_hat));
end
