.. _basis_tools:

Basis Spectra Manipulation
==========================

basis_tools
-----------
The :code:`basis_tools` script provides the user with tools for manipulating basis spectra in the FSL-MRS JSON format.

Provide one of the following subcommands with :code:`basis_tools` to convert, scale, add to, difference, or shift basis spectra.

info
****
| *Example* :code:`basis_tools info path/to/my/basis`
| Provides a short summary of the contents of the basis set.

vis
***
| *Example* :code:`basis_tools vis path/to/my/basis --ppmlim 0.2 4.2`
| Provides visualisation of the basis set.

convert
*******
| *Example* :code:`basis_tools convert path/to/my/lcmbasis.BASIS path/to/my/fslbasis`
| Convert LCModel (.Basis) or JMRUI format basis sets to FSL-MRS (.json) format.

add
***
| *Example* :code:`basis_tools add --scale --name my_new_basis my_new_basis.json path/to/my/fslbasis`
| Add a json formatted basis spectrum to an existing basis set.

shift
*****
| *Example* :code:`basis_tools shift path/to/my/fslbasis NAA 1.0 path/to/my/edited_fslbasis`
| Shift a basis spectrum on the chemical shift axis.

scale
*****
| *Example* :code:`basis_tools shift path/to/my/fslbasis NAA path/to/my/scaled_fslbasis`
| Rescale a basis spectrum to the mean of all other basis spectra (or to specified target :code:`--target_scale`.

diff
****
| *Example* :code:`basis_tools diff --add_or_sub sub mega_on mega_off mega_diff`
| Form a basis set for a difference method using two other basis set. Add or subtract using :code:`--add_or_sub {'add'|'sub}`.