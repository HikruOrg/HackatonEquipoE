import { lazy } from 'react';
import { FuseRouteItemType } from '@fuse/utils/FuseUtils';

const TalentMatcherAppView = lazy(() => import('./components/views/TalentMatcherAppView'));

/**
 * The Talent Matcher App Route.
 */
const route: FuseRouteItemType = {
	path: 'apps/talent-matcher',
	element: <TalentMatcherAppView />
};

export default route;

