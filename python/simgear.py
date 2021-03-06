"""
This is a python port of some simgear math
author: Pete Morgan - pete@freeflightsim.org

The original was a perl script By Geoff McLane
http://geoffair.org/mperl/samples/fg_server_xml2.htm
thanks Geoff! ;-)

"""

import math

SGD_PI = 3.1415926535
SGD_DEGREES_TO_RADIANS = SGD_PI / 180.0
SGD_RADIANS_TO_DEGREES = 180.0 / SGD_PI
SGD_MIN = 1.17549e-038


# Quaternion
# x,y,z,w
class Quat:
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None
		self.w = None
		
	def __repr__(self):
		return "x %s, y %s, z %s, w %s" % (rv4.x, rv4.y, rv4.z, rv4.w)
		
# Vector(3)
# x,y,z
class Vec3:
	def __init__(self):
		self.x = None
		self.y = None
		self.z = None

# Return Variables
class RetVars:
	def __init__(self):
		self.roll = None
		self.pitch = None
		self.heading = None
	def __repr__(self):
		return "roll: %s, pitch: %s, heading: %s" % (self.roll, self.pitch, self.heading)


# ============================================================ #
# SimGear Services, rendered in  Python
# ============================================================ #
# dot(const SGVec3<T>& v1, const SGVec3<T>& v2)
# { return v1(0)*v2(0) + v1(1)*v2(1) + v1(2)*v2(2); }
# Given 2 Vectors3, return the dot product
def scalar_dot_product(rv1, rv2):
	return rv1.x * rv2.x + rv1.y * rv2.y + rv1.z * rv2.z;


# The euclidean norm of the vector, that is what most people call length
# norm(const SGVec3<T>& v)
# { return sqrt(dot(v, v)); }
# Given a Vector3, return length
def norm_vector_length(rv):
	return math.sqrt(scalar_dot_product(rv, rv));


# print out a quaternion - x,y,z,w
def show_quat(rv4):
	print "x %s, y %s, z %s, w %s" % (rv4.x, rv4.y, rv4.z, rv4.w)
	

# print out a vector3
def show_vec3(rv3):
	print "x %s, y %s, z %s"  % (rv4.x, rv4.y, rv4.z)


#/// The conjugate of the quaternion, this is also the
#/// inverse for normalized quaternions
#SGQuat<T> conj(const SGQuat<T>& v)
#{ return SGQuat<T>(-v(0), -v(1), -v(2), v(3)); }
def quat_conj(rq):
	q = Quat()
	q.x =  rq.x * -1
	q.y =  rq.y * -1
	q.z =  rq.z * -1
	q.w =  rq.w 
	return q



#/// Quaternion multiplication
def mult_quats(rv1, rv2):
	q = Quat()
	q.x =  rv1.w * rv2.x + rv1.x * rv2.w + rv1.y * rv2.z - rv1.z * rv2.y
	q.y =  rv1.w * rv2.y - rv1.x * rv2.z + rv1.y * rv2.w + rv1.z * rv2.x
	q.z =  rv1.w * rv2.z + rv1.x * rv2.y - rv1.y * rv2.x + rv1.z * rv2.w
	q.w =  rv1.w * rv2.w - rv1.x * rv2.x - rv1.y * rv2.y - rv1.z * rv2.z 
	return q


#SGVec3<T> mult(const SGVec3<T>& v1, const SGVec3<T>& v2)
#{ return SGVec3<T>(v1(0)*v2(0), v1(1)*v2(1), v1(2)*v2(2)); }
"""
UNUSED ?
sub mult_vec3($$) {
	my ($rv1,$rv2) = @_;
	my @v = (0,0,0);
	$v[0] = ${$rv1}[0] * ${$rv2}[0];
	$v[1] = ${$rv1}[1] * ${$rv2}[1];
	$v[2] = ${$rv1}[2] * ${$rv2}[2];
	return \@v;
"""

#/// Scalar multiplication
#template<typename S, typename T>
# SGVec3<T> operator*(S s, const SGVec3<T>& v)
#{ return SGVec3<T>(s*v(0), s*v(1), s*v(2)); }
def scalar_mult_vector(s, rv):
	v = Vec3()
	v.x = rv.x * s 
	v.y = rv.y * s 
	v.z = rv.z * s 
	return v


#  /// write the euler angles into the references
#  void getEulerRad(T& zRad, T& yRad, T& xRad) const {
#    T sqrQW = w()*w();
#    T sqrQX = x()*x();
#    T sqrQY = y()*y();
#    T sqrQZ = z()*z();
#    T num = 2*(y()*z() + w()*x());
#    T den = sqrQW - sqrQX - sqrQY + sqrQZ;
#    if (fabs(den) <= SGLimits<T>::min() &&
#        fabs(num) <= SGLimits<T>::min())
#      xRad = 0;
#    else
#      xRad = atan2(num, den);
#    T tmp = 2*(x()*z() - w()*y());
#    if (tmp <= -1)
#      yRad = T(0.5)*SGMisc<T>::pi();
#    else if (1 <= tmp)
#      yRad = -T(0.5)*SGMisc<T>::pi();
#    else
#      yRad = -asin(tmp);
#    num = 2*(x()*y() + w()*z()); 
#    den = sqrQW + sqrQX - sqrQY - sqrQZ;
#    if (fabs(den) <= SGLimits<T>::min() &&
#        fabs(num) <= SGLimits<T>::min())
#      zRad = 0;
#    else {
#      T psi = atan2(num, den);
#      if (psi < 0)
#        psi += 2*SGMisc<T>::pi();
#      zRad = psi;
#    }
#  }
def getEulerRad(rq):

	sqrQW = rq.w * rq.w
	sqrQX = rq.x * rq.x
	sqrQY = rq.y * rq.y
	sqrQZ = rq.z * rq.z

	# y * z + w * x
	num = 2 * ( rq.y * rq.z + rq.w * rq.x )
	den = sqrQW - sqrQX - sqrQY + sqrQZ
	if abs(den) <= 0.0000001 and abs(num) <= 0.0000001:
		xRad = 0
	else:
		xRad = math.atan2(num, den)
	
	# x * z - w * y
	tmp = 2 * ( rq.x * rq.z - rq.w * rq.y )
	if tmp <= -1:
		yRad = 0.5 * SGD_PI
	elif 1 <= tmp:
		yRad = - 0.5 * SGD_PI
	else:
		yRad = -math.asin(tmp) # needs Math::Trig
	
	# x * y + w * z
	num = 2 * ( rq.x * rq.y + rq.w * rq.z ) 
	den = sqrQW + sqrQX - sqrQY - sqrQZ
	if abs(den) <= 0.0000001 and abs(num) <= 0.0000001:
		zRad = 0
	else:
		psi = math.atan2(num, den)
		if psi < 0:
			psi += 2 * SGD_PI
		zRad = psi
	
	# pass value back
	rad = Vec3()
	rad.x = xRad
	rad.y = yRad
	rad.z = zRad
	return rad


# uses getEulerRad, and converts to degrees
def getEulerDeg(rq): #, rroll, rpitch, rhead):
	rads = getEulerRad( rq )# , \$xRad, \$yRad, \$zRad)
	ob = RetVars()
	ob.heading = fgs_rad2deg(rads.z)
	ob.pitch = fgs_rad2deg(rads.y)
	ob.roll = fgs_rad2deg(rads.x)
	return ob


def fgs_rad2deg(rad):
	return rad * SGD_RADIANS_TO_DEGREES


#  static SGQuat fromRealImag(T r, const SGVec3<T>& i) {
#    SGQuat q;
#    q.w() = r;
#    q.x() = i.x();
#    q.y() = i.y();
#    q.z() = i.z();
#    return q; }
def fromRealImag(r, ri):
	q = Quat()
	q.w = r 
	q.x = ri.x
	q.y = ri.y
	q.z = ri.z
	return q


#  /// Create a quaternion from the angle axis representation where the angle
#  /// is stored in the axis' length
#  static SGQuat fromAngleAxis(const SGVec3<T>& axis) {
#    T nAxis = norm(axis);
#    if (nAxis <= SGLimits<T>::min())
#      return SGQuat::unit();
#    T angle2 = T(0.5)*nAxis;
#    return fromRealImag(cos(angle2), T(sin(angle2)/nAxis)*axis); }
def fromAngleAxis(raxis):

	nAxis = norm_vector_length(raxis);
	if nAxis <= 0.0000001:
		arr = [0,0,0,0]
		return arr # SGQuat::unit();
	
	angle2 = nAxis * 0.5
	sang = math.sin(angle2) / nAxis 
	cang = math.cos(angle2)
	rv = scalar_mult_vector(sang, raxis)
	return fromRealImag( cang, rv );


#  /// Return a quaternion rotation from the earth centered to the
#  /// simulation usual horizontal local frame from given
#  /// longitude and latitude.
#  /// The horizontal local frame used in simulations is the frame with x-axis
#  /// pointing north, the y-axis pointing eastwards and the z axis
#  /// pointing downwards.
#  static SGQuat fromLonLatRad(T lon, T lat)
#    SGQuat q;
#    T zd2 = T(0.5)*lon;
#    T yd2 = T(-0.25)*SGMisc<T>::pi() - T(0.5)*lat;
#    T Szd2 = sin(zd2);
#    T Syd2 = sin(yd2);
#    T Czd2 = cos(zd2);
#    T Cyd2 = cos(yd2);
#    q.w() = Czd2*Cyd2;
#    q.x() = -Szd2*Syd2;
#    q.y() = Czd2*Syd2;
#    q.z() = Szd2*Cyd2;
#    return q;  }
def fromLonLatRad(lonr, latr):
	zd2 = 0.5 * lonr
	yd2 = -0.25 * SGD_PI - (0.5 * latr)
	Szd2 = math.sin(zd2)
	Syd2 = math.sin(yd2)
	Czd2 = math.cos(zd2)
	Cyd2 = math.cos(yd2)
	
	q = Quat()
	q.w =  Czd2 * Cyd2
	q.x =  (Szd2 * -1) * Syd2 
	q.y =  Czd2 * Syd2 
	q.z =  Szd2 * Cyd2 
	return q


#void euler_get(float lat, float lon, float ox, float oy, float oz,
#    float *head, float *pitch, float *roll)
#{
#    /* FGMultiplayMgr::ProcessPosMsg */
#    SGVec3f angleAxis;
#    angleAxis(0) = ox;
#    angleAxis(1) = oy;
#    angleAxis(2) = oz;
#    SGQuatf ecOrient;
#    ecOrient = SGQuatf::fromAngleAxis(angleAxis);
#    /* FGAIMultiplayer::update */
#    float lat_rad, lon_rad;
#    lat_rad = lat * SGD_DEGREES_TO_RADIANS;
#    lon_rad = lon * SGD_DEGREES_TO_RADIANS;
#    SGQuatf qEc2Hl = SGQuatf::fromLonLatRad(lon_rad, lat_rad);
#    SGQuatf hlOr = conj(qEc2Hl) * ecOrient;
#    float hDeg, pDeg, rDeg;
#    hlOr.getEulerDeg(hDeg, pDeg, rDeg);
#    if(head)
#        *head = hDeg;
#    if(pitch)
#        *pitch = pDeg;
#    if(roll)
#        *roll = rDeg;
#}
def euler_get(lat, lon, ox, oy, oz):

	angleAxis = Vec3()
	angleAxis.x = ox 
	angleAxis.y = oy
	angleAxis.z = oz

	recOrient = fromAngleAxis(angleAxis) # ecOrient = SGQuatf::fromAngleAxis(angleAxis);
	#show_quat(recOrient)
	
	#/* FGAIMultiplayer::update */
	lat_rad = lat * SGD_DEGREES_TO_RADIANS
	lon_rad = lon * SGD_DEGREES_TO_RADIANS
	qEc2Hl = fromLonLatRad(lon_rad, lat_rad);
	#show_quat(qEc2Hl)
	
	con = quat_conj(qEc2Hl);
	#show_quat($con);
	
	rhlOr = mult_quats(con, recOrient);
	#show_quat($rhlOr);
	
	ob = getEulerDeg(rhlOr) #, rroll, rpitch, rhead) #, $rroll, $rpitch, $rhead )
	return ob


# ================================================================ #
# End SimGear Fuctions
# ================================================================ #