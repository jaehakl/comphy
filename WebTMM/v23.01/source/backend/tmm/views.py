import uuid, os, io, json, random, requests
import numpy as np

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.http import Http404

from .serializers import *
from .models import *

from rest_framework.permissions import IsAuthenticated

class CalculateSpectrumView(APIView):
    def post(self, request, format=None):
        layers = list(request.data.values())
        result = [["wavelength","R","T"]]

        for i in range(390, 831):        
            fm = np.array([[1,0],[0,1]])
            if len(layers) >= 2:
                depth = 0                                
                for i_layer, layer in enumerate(layers):                    
                    if i_layer < len(layers)-1:
                        tm = self.get_transfer_matrix(layers[i_layer], layers[i_layer+1],i, depth)
                        fm = np.matmul(tm,fm)
                        depth += float(layers[i_layer+1][0])
                    elif i_layer == len(layers)-1:
                        tm = self.get_transfer_matrix(layers[i_layer], [0,1,0], i, depth)
                        fm = np.matmul(tm,fm)
                r = fm[1,0]/fm[1,1]
                t = fm[0,0]-fm[0,1]*r
                result.append([i, np.abs(r)**2, np.abs(t)**2])
            else:
                result.append([i, 0, 1])
        return Response(result)

    def get_transfer_matrix(self, layer1, layer2, wavelength, depth):
        c1 = (float(layer1[1]) + 1j* float(layer1[2]))*2*np.pi/wavelength
        c2 = (float(layer2[1]) + 1j* float(layer2[2]))*2*np.pi/wavelength    

        q00 = (c2+c1)/(2*c2)*np.exp(1j*(c1-c2)*depth)
        q01 = (c2-c1)/(2*c2)*np.exp(1j*(-c2-c1)*depth)
        q10 = (c2-c1)/(2*c2)*np.exp(1j*(c2+c1)*depth)
        q11 = (c2+c1)/(2*c2)*np.exp(1j*(-c1+c2)*depth)

        return np.array([[q00,q01],[q10,q11]])


class CieAxisValueView(APIView):
    def post(self, request, format=None):
        spectra_RT = np.array(request.data[1:])
        colorFunction = np.loadtxt(
            os.path.join(
                os.path.dirname(__file__),"cie.csv"), delimiter=",")
        cie_XY_r = self.get_cie_axis(spectra_RT[:,1], colorFunction)
        cie_XY_t = self.get_cie_axis(spectra_RT[:,2], colorFunction)
        return Response({'R':cie_XY_r,'T':cie_XY_t})

    def get_cie_axis(self, spectrum, colorFunction):
        red = (spectrum*colorFunction[:,1]).mean()
        green = (spectrum*colorFunction[:,2]).mean()
        blue = (spectrum*colorFunction[:,3]).mean()
        cie_x = red/(red+green+blue)
        cie_y = green/(red+green+blue)
        return [cie_x, cie_y]

