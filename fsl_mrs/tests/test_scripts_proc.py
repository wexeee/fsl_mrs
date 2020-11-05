# Tests for the individual proc functions.
# These tests don't test theat the actual algorithms are doing the right thing,
# simply that the script handles SVS data and MRSI data properly and that the
# results from the command line program matches that of the underlying
# algorithms in preproc.py

import pytest
import os.path as op
from fsl_mrs.utils.synthetic import syntheticFID
from fsl_mrs.utils.mrs_io import fsl_io
from fsl_mrs.utils import preproc
import numpy as np
import subprocess


# construct some test data using synth
@pytest.fixture
def svs_data(tmp_path):
    reps = 3
    noiseconv = 0.1 * np.eye(reps)
    coilamps = np.ones(reps)
    coilphs = np.zeros(reps)
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    testFile = []
    data = []
    for idx, f in enumerate(FID):
        testname = f'svsdata_{idx}.nii'
        testFile.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data.append(f)
        fsl_io.saveNIFTI(testFile[idx], data[idx], hdr, affine=affine)

    return testFile, data


@pytest.fixture
def mrsi_data(tmp_path):
    reps = 3
    noiseconv = 0.1 * np.eye(reps)
    coilamps = np.ones(reps)
    coilphs = np.zeros(reps)
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    testFile = []
    data = []
    for idx, f in enumerate(FID):
        testname = f'mrsidata_{idx}.nii'
        testFile.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data.append(np.tile(f, (3, 3, 3, 1)))
        fsl_io.saveNIFTI(testFile[idx], data[idx], hdr, affine=affine)

    return testFile, data


@pytest.fixture
def svs_data_uncomb(tmp_path):
    coils = 4
    noiseconv = 0.1 * np.eye(coils)
    coilamps = np.random.randn(coils)
    coilphs = np.random.random(coils) * 2 * np.pi
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    testname = 'svsdata_uncomb.nii'
    testFile = op.join(tmp_path, testname)

    affine = np.eye(4)
    data = np.tile(np.asarray(FID).T, (1, 1, 1, 1, 1))
    fsl_io.saveNIFTI(testFile, data, hdr, affine=affine)

    return testFile, data


@pytest.fixture
def mrsi_data_uncomb(tmp_path):
    coils = 4
    noiseconv = 0.1 * np.eye(coils)
    coilamps = np.random.randn(coils)
    coilphs = np.random.random(coils) * 2 * np.pi
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    testname = 'mrsidata_uncomb.nii'
    testFile = op.join(tmp_path, testname)

    affine = np.eye(4)
    data = np.tile(np.asarray(FID).T, (3, 3, 3, 1, 1))
    fsl_io.saveNIFTI(testFile, data, hdr, affine=affine)

    return testFile, data


@pytest.fixture
def svs_data_diff(tmp_path):
    reps = 2
    noiseconv = 0.1 * np.eye(reps)
    coilamps = np.ones(reps)
    coilphs = np.zeros(reps)
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    coilamps = np.ones(reps)
    coilphs = np.random.randn(reps)
    FID2, hdr = syntheticFID(noisecovariance=noiseconv,
                             coilamps=coilamps,
                             coilphase=coilphs)

    testFile, testFile2 = [], []
    data, data2 = [], []
    for idx, f in enumerate(FID):
        testname = f'svsdata_0_{idx}.nii'
        testFile.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data.append(f)
        fsl_io.saveNIFTI(testFile[idx], data[idx], hdr, affine=affine)

    for idx, f in enumerate(FID2):
        testname = f'svsdata_1_{idx}.nii'
        testFile2.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data2.append(f)
        fsl_io.saveNIFTI(testFile2[idx], data2[idx], hdr, affine=affine)

    return testFile, testFile2, data, data2


@pytest.fixture
def mrsi_data_diff(tmp_path):
    reps = 2
    noiseconv = 0.1 * np.eye(reps)
    coilamps = np.ones(reps)
    coilphs = np.zeros(reps)
    FID, hdr = syntheticFID(noisecovariance=noiseconv,
                            coilamps=coilamps,
                            coilphase=coilphs)

    coilamps = np.ones(reps)
    coilphs = np.random.randn(reps)
    FID2, hdr = syntheticFID(noisecovariance=noiseconv,
                             coilamps=coilamps,
                             coilphase=coilphs)

    testFile, testFile2 = [], []
    data, data2 = [], []
    for idx, f in enumerate(FID):
        testname = f'mrsidata_{idx}.nii'
        testFile.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data.append(np.tile(f, (3, 3, 3, 1)))
        fsl_io.saveNIFTI(testFile[idx], data[idx], hdr, affine=affine)

    for idx, f in enumerate(FID2):
        testname = f'mrsidata_{idx}.nii'
        testFile2.append(op.join(tmp_path, testname))

        affine = np.eye(4)
        data2.append(np.tile(f, (3, 3, 3, 1)))
        fsl_io.saveNIFTI(testFile2[idx], data2[idx], hdr, affine=affine)

    return testFile, testFile2, data, data2


def splitdata(svs, mrsi):
    return svs[0], mrsi[0], svs[1], mrsi[1]


def test_filecreation(svs_data, mrsi_data, svs_data_uncomb, mrsi_data_uncomb):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    data, hdr = fsl_io.readNIFTI(svsfile[0], squeezeSVS=False)
    assert data.shape == (1, 1, 1, 2048)
    assert np.isclose(data, svsdata[0]).all()

    data, hdr = fsl_io.readNIFTI(mrsifile[0], squeezeSVS=False)
    assert data.shape == (3, 3, 3, 2048)
    assert np.isclose(data, mrsidata[0]).all()

    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data_uncomb,
                                                     mrsi_data_uncomb)

    data, hdr = fsl_io.readNIFTI(svsfile, squeezeSVS=False)
    assert data.shape == (1, 1, 1, 2048, 4)
    assert np.isclose(data, svsdata).all()

    data, hdr = fsl_io.readNIFTI(mrsifile, squeezeSVS=False)
    assert data.shape == (3, 3, 3, 2048, 4)
    assert np.isclose(data, mrsidata).all()


def test_coilcombine(svs_data_uncomb, mrsi_data_uncomb, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data_uncomb,
                                                     mrsi_data_uncomb)

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'coilcombine',
                           '--file', svsfile,
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.combine_FIDs(svsdata[0, 0, 0, ...],
                                     'svd',
                                     do_prewhiten=True)

    assert np.isclose(data, directRun).all()

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'coilcombine',
                           '--file', mrsifile,
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.combine_FIDs(mrsidata[2, 2, 2, ...], 'svd',
                                     do_prewhiten=True)

    assert np.isclose(data[2, 2, 2, ...], directRun).all()


def test_average(svs_data, mrsi_data, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'average',
                           '--file', svsfile[0], svsfile[1], svsfile[2],
                           '--avgfiles',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    allFileData = np.array([d for d in svsdata])
    directRun = preproc.combine_FIDs(allFileData.T, 'mean')

    assert np.isclose(data, directRun).all()

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'average',
                           '--file', mrsifile[0], mrsifile[1], mrsifile[2],
                           '--avgfiles',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    allFileData = np.array([d for d in mrsidata])
    directRun = preproc.combine_FIDs(allFileData.T, 'mean')

    assert np.isclose(data, directRun).all()


def test_align(svs_data, mrsi_data, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run align on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'align',
                           '--file', svsfile[0], svsfile[1], svsfile[2],
                           '--ppm', '-10', '10',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp_000.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    allFileData = [d for d in svsdata]
    directRun, _, _ = preproc.phase_freq_align(allFileData,
                                               4000,
                                               123.2E6,
                                               niter=2,
                                               ppmlim=[-10.0, 10.0],
                                               verbose=False,
                                               target=None,
                                               apodize=10)

    assert np.allclose(data, directRun[0])

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'align',
                           '--file', mrsifile[0], mrsifile[1], mrsifile[2],
                           '--ppm', '-10', '10',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp_000.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    allFileData = [d[2, 2, 2, ...] for d in mrsidata[0:3]]
    directRun, _, _ = preproc.phase_freq_align(allFileData,
                                               4000,
                                               123.2E6,
                                               niter=2,
                                               ppmlim=[-10.0, 10.0],
                                               verbose=False,
                                               target=None,
                                               apodize=10)

    assert np.allclose(data[2, 2, 2, ...], directRun[0],
                       atol=1E-1, rtol=1E-1)


def test_ecc(svs_data, mrsi_data, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'ecc',
                           '--file', svsfile[0],
                           '--reference', svsfile[1],
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.eddy_correct(svsdata[0], svsdata[1])

    assert np.isclose(data, directRun).all()

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'ecc',
                           '--file', mrsifile[0],
                           '--reference', mrsifile[1],
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.eddy_correct(mrsidata[0][2, 2, 2, ...],
                                     mrsidata[1][2, 2, 2, ...])

    assert np.isclose(data[2, 2, 2, ...], directRun).all()


def test_remove(svs_data, mrsi_data, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run remove on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'remove',
                           '--file', svsfile[0],
                           '--ppm', '-10', '10',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    limits = (-10, 10)
    directRun = preproc.hlsvd(svsdata[0],
                              1 / 4000,
                              123.2,
                              limits,
                              limitUnits='ppm+shift')

    assert np.isclose(data, directRun).all()

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'remove', '--file',
                           mrsifile[0],
                           '--ppm', '-10', '10',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    limits = (-10, 10)
    directRun = preproc.hlsvd(mrsidata[0][2, 2, 2, ...],
                              1 / 4000.0,
                              123.2,
                              limits,
                              limitUnits='ppm+shift')

    assert np.isclose(data[2, 2, 2, ...], directRun).all()


def test_align_diff(svs_data_diff, mrsi_data_diff, tmp_path):
    svsfile1, svsfile2, svsdata1, svsdata2 = svs_data_diff[0], \
        svs_data_diff[1], \
        svs_data_diff[2], \
        svs_data_diff[3]
    # mrsifile1, mrsifile2, mrsidata1, mrsidata2 = mrsi_data_diff[0], \
    #                                              mrsi_data_diff[1], \
    #                                              mrsi_data_diff[2], \
    #                                              mrsi_data_diff[3]

    # Run alignment via commandline
    subprocess.check_call(['fsl_mrs_proc',
                           'align-diff',
                           '--file', svsfile1[0], svsfile1[1],
                           '--reference', svsfile2[0], svsfile2[1],
                           '--ppm', '-10', '10',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp_000.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun, _, _, _ = preproc.phase_freq_align_diff(svsdata1,
                                                       svsdata2,
                                                       4000,
                                                       123.2E6,
                                                       ppmlim=[-10.0, 10.0])

    assert np.isclose(data, directRun[0]).all()
    # TODO: finish MRSI test


def test_fshift(svs_data, mrsi_data, tmp_path):
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    subprocess.check_call(['fsl_mrs_proc',
                           'fshift',
                           '--file', svsfile[0],
                           '--shiftppm', '1.0',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.freqshift(svsdata[0], 1 / 4000, 1.0 * 123.2)

    assert np.allclose(data, directRun)

    subprocess.check_call(['fsl_mrs_proc',
                           'fshift',
                           '--file', svsfile[0],
                           '--shiftRef',
                           '--ppm', '-5.0', '5.0',
                           '--target', '4.0',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun, _ = preproc.shiftToRef(svsdata[0],
                                      4.0,
                                      4000.0,
                                      123.2E6,
                                      ppmlim=(-5.0, 5.0))

    assert np.allclose(data, directRun)
    # TODO: finish MRSI test


def test_conj(svs_data, mrsi_data, tmp_path):
    """ Test fsl_mrs_proc conj"""
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run remove on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'conj',
                           '--file', svsfile[0],
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using numpy directly
    directRun = np.conj(svsdata[0])

    assert np.allclose(data, directRun)

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'conj',
                           '--file', mrsifile[0],
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = np.conj(mrsidata[0][2, 2, 2, ...])

    assert np.allclose(data[2, 2, 2, ...], directRun)


def test_fixed_phase(svs_data, mrsi_data, tmp_path):
    """ Test fsl_mrs_proc fixed_phase"""
    svsfile, mrsifile, svsdata, mrsidata = splitdata(svs_data, mrsi_data)

    # Run remove on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'fixed_phase',
                           '--file', svsfile[0],
                           '--p0', '90',
                           '--p1', '0.001',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using numpy directly
    directRun = preproc.applyPhase(svsdata[0],
                                   (np.pi / 180.0) * 90)

    directRun, newDT = preproc.timeshift(
        directRun,
        1 / 4000,
        0.001,
        0.001,
        samples=directRun.size)

    assert np.allclose(data, directRun)

    # Run coil combination on both sets of data using the command line
    subprocess.check_call(['fsl_mrs_proc',
                           'fixed_phase',
                           '--file', mrsifile[0],
                           '--p0', '90',
                           '--p1', '0.001',
                           '--output', tmp_path,
                           '--filename', 'tmp'])

    # Load result for comparison
    data, hdr = fsl_io.readNIFTI(op.join(tmp_path, 'tmp.nii.gz'),
                                 squeezeSVS=True)

    # Run using preproc.py directly
    directRun = preproc.applyPhase(mrsidata[0][2, 2, 2, ...],
                                   (np.pi / 180.0) * 90)

    directRun, newDT = preproc.timeshift(
        directRun,
        1 / 4000,
        0.001,
        0.001,
        samples=directRun.size)

    assert np.allclose(data[2, 2, 2, ...], directRun)
