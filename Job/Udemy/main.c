#include <stdio.h>
#include <stdlib.h>
#include <math.h>

#define SIG_LENGTH 320
#define IMP_RESP_LENGTH 29

// Signal is saved in "waveforms.c"
extern double InputSignal_f32_1kHz_15kHz[SIG_LENGTH];
extern double  Impulse_response[IMP_RESP_LENGTH];

// Function Signatures
double calc_sig_mean(double *sig_src_array, int sig_length);
double calc_sig_sd(double *sig_src_array, double sig_mean, int sig_length);
void convolution(double *sig_src_arr,
                 double *sig_dest_arr,
                 double *imp_response_arr,
                 int sig_src_length,
                 int imp_response_length
                 );

// Variables
double output_signal[SIG_LENGTH+IMP_RESP_LENGTH-1];

int main()
{
    printf("~~ DSP in C, powered by Udemy ~~\n");

    convolution(&InputSignal_f32_1kHz_15kHz[0],
                &output_signal[0],
                &Impulse_response[0],
                SIG_LENGTH,
                IMP_RESP_LENGTH
                 );

    FILE *input_sig_fptr, *imp_rsp_fptr, *output_sig_fptr;

    input_sig_fptr = fopen("input_signal.dat","w");
    imp_rsp_fptr = fopen("impulse_response.dat","w");
    output_sig_fptr = fopen("output_signal.dat","w");

    for (int i=0; i<SIG_LENGTH; i++)
    {
        fprintf(input_sig_fptr,"\n%f",InputSignal_f32_1kHz_15kHz[i]);

    }
    fclose(input_sig_fptr);

    for (int i=0; i<IMP_RESP_LENGTH;i++)
    {
        fprintf(imp_rsp_fptr,"\n%f",Impulse_response[i]);
    }
    fclose(imp_rsp_fptr);

    for (int i=0; i<(SIG_LENGTH+IMP_RESP_LENGTH-1); i++)
    {
        fprintf(output_sig_fptr,"\n%f", output_signal[i]);
    }
    fclose(output_sig_fptr);

    return 0;
}

// Function to calculate signal mean
double calc_sig_mean(double *sig_src_array, int sig_length)
{
    double _mean = 0.0;
    for (int i=0; i<sig_length; i++)
    {
        _mean = _mean + sig_src_array[i];
    }
    _mean = _mean/(double)sig_length;
    return _mean;
}

// Function to calculate signal standard deviation
double calc_sig_sd(double *sig_src_array, double sig_mean, int sig_length)
{
    double _sd = 0.0;
    for (int i=0; i<sig_length; i++)
    {
        _sd = _sd + pow((sig_src_array[i] - sig_mean),2);
    }
    _sd  = sqrt(_sd/(double)(sig_length-1));
    return _sd;
}

// Function to calculate the convolution of two signals
void convolution(double *sig_src_arr,
                 double *sig_dest_arr,
                 double *imp_response_arr,
                 int sig_src_length,
                 int imp_response_length
                 )
{
    int i,j;
    for (i=0; i<(sig_src_length+imp_response_length-1); i++)
    {
        sig_dest_arr[i] = 0;

    }

    for (i=0; i<sig_src_length; i++)
    {
        for(j=0; j<imp_response_length; j++)
        {
            sig_dest_arr[i+j] = sig_dest_arr[i+j] + (sig_src_arr[i] * imp_response_arr[j]);
        }
    }
}

// ?
